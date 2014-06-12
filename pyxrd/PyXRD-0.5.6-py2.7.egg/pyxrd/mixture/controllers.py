# coding=UTF-8
# ex:ts=4:sw=4:et=on

# Copyright (c) 2013, Mathijs Dumon
# All rights reserved.
# Complete license can be found in the LICENSE file.

import gtk

from pyxrd.mvc import Controller, Observer

from pyxrd.generic.views.treeview_tools import new_text_column, new_pb_column, new_toggle_column
from pyxrd.generic.mathtext_support import create_pb_from_mathtext
from pyxrd.generic.controllers import DialogController, BaseController, ObjectListStoreController

from pyxrd.mixture.models.parspace import ParameterSpaceGenerator
from pyxrd.mixture.models import Mixture
from pyxrd.mixture.views import EditMixtureView, RefinementView, RefinementResultView
from pyxrd.generic.controllers.objectliststore_controllers import wrap_list_property_to_treemodel
from contextlib import contextmanager

class RefinementResultsController(DialogController):
    """
        A controller for a RefinementContext object that keeps track
        of the solutions and residuals generated by the refinement
        algorithm. This allows to show a nice dialog with the end
        results and some graphs about the parameter space.
    """

    auto_adapt = True
    auto_adapt_included = [
        "initial_residual",
        "last_residual",
        "best_residual"
    ]
    solutions = None

    # ------------------------------------------------------------
    #      Initialisation and other internals
    # ------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(RefinementResultsController, self).__init__(*args, **kwargs)
        self.parspace_gen = ParameterSpaceGenerator()
        self.parspace_gen.initialize(self.model.ranges, 199)

    # ------------------------------------------------------------
    #      Notifications of observable properties
    # ------------------------------------------------------------
    @Controller.observe("solution_added", signal=True)
    def notif_solution_added(self, model, prop_name, info):
        if self.model.mixture.make_psp_plots:
            new_solution, new_residual = info.arg
            self.parspace_gen.record(new_solution, new_residual)

    # ------------------------------------------------------------
    #      GTK Signal handlers
    # ------------------------------------------------------------
    def on_btn_initial_clicked(self, event):
        self.model.apply_initial_solution()
        self.model.mixture.refiner.delete_context()
        self.on_cancel()
        return True

    def on_btn_best_clicked(self, event):
        self.model.apply_best_solution()
        self.model.mixture.refiner.delete_context()
        self.on_cancel()
        return True

    def on_btn_last_clicked(self, event):
        self.model.apply_last_solution()
        self.model.mixture.refiner.delete_context()
        self.on_cancel()
        return True

    # ------------------------------------------------------------
    #      Methods & Functions
    # ------------------------------------------------------------
    def generate_images(self, output_dir="", density=200):
        """
            Generate the parameter space plots
        """
        self.parspace_gen.plot_images(
            figure=self.view.figure,
            centroid=self.model.best_solution,
            labels=[ref_prop.title for ref_prop in self.model.ref_props],
            density=density
        )

    def clear_images(self):
        self.parspace_gen.clear_image(figure=self.view.figure)

    pass # end of class

class RefinementController(DialogController):

    auto_adapt_included = [
        "refine_method",
        "refinables",
        "make_psp_plots",
    ]

    @property
    def treemodel(self):
        return self.model.refinables

    def setup_refinables_tree_view(self, store, widget):
        """
            Setup refinables TreeView layout
        """
        widget.set_show_expanders(True)

        # Labels are parsed for mathtext markup into pb's:
        def get_pb(column, cell, model, itr, user_data=None):
            ref_prop = model.get_user_data(itr)
            if not hasattr(ref_prop, "pb") or not ref_prop.pb:
                ref_prop.pb = create_pb_from_mathtext(
                    ref_prop.title,
                    align='left',
                    weight='medium'
                )
            cell.set_property("pixbuf", ref_prop.pb)
            return
        widget.append_column(new_pb_column('Name/Prop', xalign=0.0, data_func=get_pb))

        # Editable floats:
        def get_value(column, cell, model, itr, *args):
            col = column.get_col_attr('markup')
            try:
                value = model.get_value(itr, col)
                value = "%.5f" % value
            except TypeError: value = ""
            cell.set_property("markup", value)
            return
        def on_float_edited(rend, path, new_text, model, col):
            itr = model.get_iter(path)
            try:
                model.set_value(itr, col, float(new_text))
            except ValueError:
                return False
            return True

        def_float_args = {
            "sensitive_col": store.c_refinable,
            "editable_col": store.c_refinable,
            "visible_col": store.c_refinable,
            "data_func": get_value
        }

        widget.append_column(new_text_column(
            "Value", markup_col=store.c_value,
            edited_callback=(
                on_float_edited,
                (store, store.c_value,)
            ), **def_float_args
        ))
        widget.append_column(new_text_column(
            "Min", markup_col=store.c_value_min,
            edited_callback=(
                on_float_edited,
                (store, store.c_value_min,)
            ), **def_float_args
        ))
        widget.append_column(new_text_column(
            "Max", markup_col=store.c_value_max,
            edited_callback=(
                on_float_edited,
                (store, store.c_value_max,)
            ), **def_float_args
        ))

        # The 'refine' checkbox:
        widget.append_column(new_toggle_column(
            "Refine",
            toggled_callback=(self.refine_toggled, (store,)),
            resizable=False,
            expand=False,
            active_col=store.c_refine,
            sensitive_col=store.c_refinable,
            activatable_col=store.c_refinable,
            visible_col=store.c_refinable
        ))

    def _update_method_options_store(self):
        """
            Update the method options tree store (when a new method is selected)
        """
        # 1 get the method:
        refine_method = self.model.get_refinement_method()

        # 2 get the options:
        options = refine_method.options

        tv = self.view['tv_method_options']

        # 3 make a liststore
        store = gtk.ListStore(str, object, str, object, object, object)
        for name, arg, typ, default, limits in options:
            store.append([name, default, arg, typ, default, limits])

        tv.set_model(store)

        return tv

    def _setup_method_options_treeview(self):
        """
            Initial method options tree view layout & behavior setup
        """
        # Update the method options store to match the currently selected
        # refinement method
        tv = self._update_method_options_store()

        # The name of the option:
        tv.append_column(new_text_column("Name", text_col=0))

        # The value of the option:
        def get_value(column, cell, model, itr, *args):
            name, value, arg, typ, default, limits = tv.get_model().get(itr, 0, 1, 2, 3, 4, 5)
            if typ in (int, float, str):
                value = str(value)
                cell.set_property("sensitive", True)
                cell.set_property("editable", True)
            else:
                value = ""
                cell.set_property("sensitive", False)
                cell.set_property("editable", False)
            cell.set_property("markup", value)
            return
        def on_value_edited(rend, path, new_text, col):
            store = tv.get_model()
            itr = store.get_iter(path)
            name, value, arg, typ, default, limits = store.get(itr, 0, 1, 2, 3, 4, 5)
            if typ in (int, float, str):
                try:
                    value = typ(new_text)
                    if typ in (int, float,):
                        min_value, max_value = limits
                        if min_value is not None: value = max(min_value, value)
                        if max_value is not None: value = min(max_value, value)
                        store.set_value(itr, col, value)
                    elif limits is not None:
                        if value in limits:
                            store.set_value(itr, col, value)
                        else:
                            raise ValueError
                except ValueError:
                    pass
            else:
                pass
            return True
        tv.append_column(new_text_column(
            "Value", text_col=1,
            data_func=get_value,
            edited_callback=(on_value_edited, (1,)),
        ))

        # An optional checkbox:
        def get_check_value(column, cell, model, itr, *args):
            name, value, arg, typ, default, limits = tv.get_model().get(itr, 0, 1, 2, 3, 4, 5)
            if typ in (bool,):
                value = bool(value)
                cell.set_property("active", value)
                cell.set_property("visible", True)
                cell.set_property("sensitive", True)
                cell.set_property("activatable", True)
            else:
                cell.set_property("visible", False)
                cell.set_property("sensitive", False)
                cell.set_property("activatable", False)
            return
        def on_value_toggled(cell, path, col):
            store = tv.get_model()
            itr = store.get_iter(path)
            name, value, arg, typ, default, limits = store.get(itr, 0, 1, 2, 3, 4, 5)
            if typ in (bool,):
                store.set_value(itr, col, cell.get_active())
            else:
                pass
            return True

        tv.append_column(new_toggle_column(
                "",
                data_func=get_check_value,
                toggled_callback=(on_value_toggled, (1,)),
                resizable=False,
                expand=False
        ))

    def register_view(self, view):
        self._setup_method_options_treeview()

    # ------------------------------------------------------------
    #      Notifications of observable properties
    # ------------------------------------------------------------
    @Observer.observe("refine_method", assign=True)
    def on_prop_changed(self, model, prop_name, info):
        self._update_method_options_store()

    # ------------------------------------------------------------
    #      GTK Signal handlers
    # ------------------------------------------------------------
    def on_cancel(self):
        if not self.model.refiner.refine_lock:
            self.view.hide()
        else:
            return True # do nothing

    def refine_toggled(self, cell, path, model):
        if model is not None:
            itr = model.get_iter(path)
            model.set_value(itr, model.c_refine, not cell.get_active())
        return True

    def on_btn_randomize_clicked(self, event):
        self.model.randomize()

    def on_auto_restrict_clicked(self, event):
        self.model.auto_restrict()

    @DialogController.status_message("Refining mixture...", "refine_mixture")
    def on_refine_clicked(self, event):

        # Make sure we can refine:
        if len(self.model.specimens) > 0:
            # Setup mixture based on chosen refinement options:
            self.model.refine_options = {}
            option_store = self.view['tv_method_options'].get_model()
            for name, value, arg, typ, default, limits in option_store: # @UnusedVariable
                self.model.refine_options[arg] = value

            # Setup context and results controller:
            self.model.refiner.setup_context(store=True)
            self.results_view = RefinementResultView(parent=self.view.parent)
            self.results_controller = RefinementResultsController(
                model=self.model.refiner.context,
                view=self.results_view,
                parent=self
            )

            # Run the refinement thread:
            self.view.show_refinement_info(
                self.model.refiner.refine, # REFINE METHOD
                self.update_gui,      # GUI UPDATER
                self.on_complete           # ON COMPLETE CALLBACK
            )
        else:
            self.run_information_dialog("Cannot refine an empty mixture!", parent=self.view.get_toplevel())

    def on_complete(self, context, *args, **kwargs):
        self.model.refiner.context.status_message = "Generating parameter space plots..."
        if self.model.make_psp_plots:
            self.results_controller.generate_images()
        self.results_view.present()
        self.view.hide()

    def update_gui(self):
        self.view.update_refinement_info(
            self.model.refiner.context.last_residual,
            self.model.refiner.context.status_message
        )

    def cleanup(self):
        if hasattr(self, "view"):
            del self.view
        if hasattr(self, "results_view"):
            del self.results_view
        if hasattr(self, "results_controller"):
            del self.results_controller
        if hasattr(self, "model"):
            self.relieve_model(self.model)

    pass # end of class

class EditMixtureController(BaseController):

    auto_adapt_excluded = [
        "refine_method",
        "refinables",
        "make_psp_plots"
    ]

    ref_view = None

    @property
    def specimens_treemodel(self):
        prop = self.model.project.Meta.get_prop_intel_by_name("specimens")
        return wrap_list_property_to_treemodel(self.model.project, prop)

    @property
    def phases_treemodel(self):
        prop = self.model.project.Meta.get_prop_intel_by_name("phases")
        return wrap_list_property_to_treemodel(self.model.project, prop)

    def register_adapters(self):
        self.create_ui()

    def create_ui(self):
        """
            Creates a complete new UI for the Mixture model
        """
        self.view.reset_view()
        for index in range(len(self.model.phases)):
            self._add_phase_view(index)
        for index in range(len(self.model.specimens)):
            self._add_specimen_view(index)

    def _add_phase_view(self, phase_slot):
        """
            Adds a new view for the given phase slot.
        """
        def on_label_changed(editable):
            self.model.phases[phase_slot] = editable.get_text()

        def on_fraction_changed(editable):
            try: self.model.fractions[phase_slot] = float(editable.get_text())
            except ValueError: return # ignore ValueErrors

        def on_phase_delete(widget):
            self.model.del_phase_slot(phase_slot)
            widget.disconnect(widget.get_data("deleventid"))

        self.view.add_phase_slot(self.phases_treemodel,
            on_phase_delete, on_label_changed, on_fraction_changed,
            self.on_combo_changed, label=self.model.phases[phase_slot],
            fraction=self.model.fractions[phase_slot], phases=self.model.phase_matrix)

    def _add_specimen_view(self, specimen_slot):
        """
            Adds a new view for the given specimen slot
        """
        def on_scale_changed(editable):
            try: self.model.scales[specimen_slot] = float(editable.get_text())
            except ValueError: return # ignore ValueErrors

        def on_bgs_changed(editable):
            try: self.model.bgshifts[specimen_slot] = float(editable.get_text())
            except ValueError: return # ignore ValueErrors

        def on_specimen_changed(combobox):
            itr = combobox.get_active_iter()
            specimen = self.specimens_treemodel.get_user_data(itr) if itr is not None else None
            self.model.set_specimen(specimen_slot, specimen)

        def on_specimen_delete(widget):
            self.model.del_specimen_slot(specimen_slot)
            widget.disconnect(widget.get_data("deleventid"))

        self.view.add_specimen_slot(self.phases_treemodel,
            self.specimens_treemodel, on_specimen_delete, on_scale_changed,
            on_bgs_changed, on_specimen_changed, self.on_combo_changed,
            scale=self.model.scales[specimen_slot], bgs=self.model.bgshifts[specimen_slot],
            specimen=self.model.specimens[specimen_slot], phases=self.model.phase_matrix)

    # ------------------------------------------------------------
    #      Notifications of observable properties
    # ------------------------------------------------------------
    @Controller.observe("data_changed", signal=True)
    def notif_has_changed(self, model, prop_name, info):
        self.view.update_all(self.model.fractions, self.model.scales, self.model.bgshifts)

    @Controller.observe("needs_reset", signal=True)
    def notif_needs_reset(self, model, prop_name, info):
        self.create_ui()

    # ------------------------------------------------------------
    #      GTK Signal handlers
    # ------------------------------------------------------------
    def on_combo_changed(self, combobox, row, col):
        itr = combobox.get_active_iter()
        phase = self.phases_treemodel.get_user_data(itr) if itr is not None else None
        self.model.set_phase(row, col, phase)

    def on_add_phase(self, widget, *args):
        with self.model.data_changed.hold():
            index = self.model.add_phase_slot("New Phase", 1.0)
            self._add_phase_view(index)

    def on_add_specimen(self, widget, *args):
        with self.model.data_changed.hold():
            index = self.model.add_specimen_slot(None, 1.0, 0.0)
            self._add_specimen_view(index)

    def on_add_both(self, widget, *args):
        with self.model.data_changed.hold():
            self.on_add_specimen(widget, *args)
            self.on_add_phase(widget, *args)

    def on_optimize_clicked(self, widget, *args):
        self.model.optimize()

    def on_refine_clicked(self, widget, *args):
        self.model.update_refinement_treestore()
        if self.ref_view is not None:
            self.ref_view.hide()
            self.ref_ctrl.cleanup()
        self.ref_view = RefinementView(parent=self.parent.view)
        self.ref_ctrl = RefinementController(model=self.model, view=self.ref_view, parent=self)
        self.ref_view.present()

    def on_composition_clicked(self, widget, *args):
        comp = "The composition of the specimens in this mixture:\n\n\n"
        comp += "<span font-family=\"monospace\">"
        # get the composition matrix (first columns contains strings with elements, others are specimen compositions)
        import re
        for row in self.model.get_composition_matrix():
            comp += "%s %s\n" % (re.sub(r'(\d+)', r'<sub>\1</sub>', row[0]), " ".join(row[1:]))
        comp += "</span>"
        self.run_information_dialog(comp, parent=self.view.get_toplevel())

    pass # end of class

class MixturesController(ObjectListStoreController):

    treemodel_property_name = "mixtures"
    treemodel_class_type = Mixture
    columns = [ ("Mixture name", "c_name") ]
    delete_msg = "Deleting a mixture is irreverisble!\nAre You sure you want to continue?"
    obj_type_map = [
        (Mixture, EditMixtureView, EditMixtureController),
    ]

    def get_mixtures_tree_model(self, *args):
        return self.treemodel

    # ------------------------------------------------------------
    #      GTK Signal handlers
    # ------------------------------------------------------------
    def on_load_object_clicked(self, event):
        pass # cannot load mixtures
    def on_save_object_clicked(self, event):
        pass # cannot save mixtures

    def create_new_object_proxy(self):
        return Mixture(parent=self.model)

    @contextmanager
    def _multi_operation_context(self):
        with self.model.data_changed.hold():
            yield

    pass # end of class
