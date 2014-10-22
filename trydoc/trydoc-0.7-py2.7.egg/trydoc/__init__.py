# -*- coding: utf-8 -*-
"""
    trydoc
    ------

    :copyright: Copyright 2012-14 by NaN Projectes de Programari Lliure, S.L.
    :license: BSD, see LICENSE for details.
"""
from path import path
import ConfigParser
import os
import re
import simplejson
import sys
import tempfile
import time

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Image
from docutils.transforms import Transform
from sphinx.util.compat import Directive

import proteus
try:
    import gtk
    import gobject
    import signal
    import tryton
except ImportError, e:
    print >> sys.stderr, ("gtk importation error (%s). Screenshots feature "
        "will not be available.") % e
    gtk = None
    gobject = None
    tryton = None


screenshot_files = []


def get_model_data(model_name, show_info):
    if not proteus.config._CONFIG.current:
        raise ValueError('Proteus has not been initialized.')

    Model = proteus.Model.get('ir.model')
    models = Model.find([
            ('model', '=', model_name),
            ])
    if not models:
        return None

    text = models[0].name if not show_info else models[0].info
    return text


def get_field_data(model_name, field_name, show_help):
    if not proteus.config._CONFIG.current:
        raise ValueError('Proteus has not been initialized.')

    Model = proteus.Model.get('ir.model')
    models = Model.find([
            ('model', '=', model_name),
            ])
    if not models:
        return None

    ModelField = proteus.Model.get('ir.model.field')
    fields = ModelField.find([
            ('name', '=', field_name),
            ('model', '=', models[0].id),
            ], limit=1)
    if not fields:
        raise AttributeError('Model "%s" has no field named "%s"'
            % (model_name, field_name))
    field, = fields

    text = ''
    if show_help:
        if field.help:
            text = field.help
        else:
            text = 'Field "%s" has no help available' % field.name
    else:
        if field.field_description:
            text = field.field_description
        else:
            text = ('Field "%s" has no description available'
                % field.name)
    return text


def get_ref_data(module_name, fs_id, field=None):
    if not proteus.config._CONFIG.current:
        raise ValueError('Proteus has not been initialized.')
    ModelData = proteus.Model.get('ir.model.data')

    records = ModelData.find([
            ('module', '=', module_name),
            ('fs_id', '=', fs_id),
            ])
    if not records:
        return None

    db_id = records[0].db_id
    # model cannot be unicode
    model = str(records[0].model)

    Model = proteus.Model.get(model)
    record = Model(db_id)
    if field:
        return getattr(record, field)
    return record


class ModelDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'info': directives.flag,
        'class': directives.class_option,
        }
    has_content = False

    def run(self):
        config = self.state.document.settings.env.config
        if 'info' in self.options:
            show_info = True
        else:
            show_info = False
        classes = [config.trydoc_modelclass]
        if 'class' in self.options:
            classes.extend(self.options['class'])

        model_name = self.arguments[0]
        text = get_model_data(model_name, show_info)
        if text is None:
            return [self.state_machine.reporter.warning(
                    'Model "%s" not found.' % model_name, line=self.lineno)]

        return [nodes.inline(text, text, classes=classes)]


class FieldDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'help': directives.flag,
        'class': directives.class_option,
        }
    has_content = False

    def run(self):
        config = self.state.document.settings.env.config
        if 'help' in self.options:
            show_help = True
        else:
            show_help = False
        classes = [config.trydoc_fieldclass]
        if 'class' in self.options:
            classes.extend(self.options['class'])

        model_name, field_name = self.arguments[0].split('/')
        text = get_field_data(model_name, field_name, show_help)
        if text is None:
            return [self.state_machine.reporter.warning(
                    'Model "%s" not found.' % model_name, line=self.lineno)]

        return [nodes.inline(text, text, classes=classes)]


class TryRefDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'class': directives.class_option,
        }
    has_content = False

    def run(self):
        config = self.state.document.settings.env.config
        classes = [config.trydoc_refclass]
        if 'class' in self.options:
            classes.extend(self.options['class'])

        ref, field = self.arguments[0].split('/')
        module_name, fs_id = ref.split('.')

        text = get_ref_data(module_name, fs_id, field)
        if text is None:
            return [self.state_machine.reporter.warning(
                    'Reference "%s" not found.' % content, line=self.lineno)]

        return [nodes.inline(text, text, classes=classes)]


class ViewDirective(Image):
    # Directive attributes
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = Image.option_spec.copy()
    option_spec.update({
        'field': directives.unchanged,
        'domain': directives.unchanged,
        'show_menu': directives.unchanged,
        })
    # Class attributes
    trytond_host = None
    trytond_port = None
    trytond_dbname = None
    trytond_user = None
    trytond_password = None
    tryton_default_width = 2048
    tryton_default_height = 1024
    tryton_main = None
    tryton_prefs = None
    # Instance attributes
    filename = None

    def run(self):
        assert gtk is not None, "gtk not imported"
        assert gobject is not None, "gobject not imported"
        assert tryton is not None, "tryton not imported"

        env = self.state.document.settings.env
        if 'class' in self.options:
            self.options['class'].insert(0, env.config.trydoc_viewclass)
        else:
            self.options['class'] = [env.config.trydoc_viewclass]

        view_xml_id = str(self.arguments[0])
        field_name = self.options.get('field')
        domain = self.options.get('domain')
        try:
            if domain:
                domain = domain.replace("'", '"')
                simplejson.loads(domain)
        except ValueError:
            env.warn(env.docname, "Invalid domain expression in view "
                "directive. It isn't generated.", self.lineno)
            return []

        tryton_main = self.get_tryton_main()

        url = self.calc_url(view_xml_id, domain=domain)
        if not url:
            return []

        source_document_path = path(self.state.document.current_source)
        prefix = 'screenshot-' + source_document_path.basename().split('.')[0]
        _, self.filename = tempfile.mkstemp(prefix=prefix,
            suffix='.png', dir=source_document_path.parent)

        self.screenshot(tryton_main, url, field_name)
        screenshot_files.append(self.filename)

        # if app.config.verbose:
        if env.app:
            env.app.info("Screenshot %s in tempfile %s"
                % (url, self.filename))
        else:
            sys.stdout.write("INFO: Screenshot %s in tempfile %s\n"
                % (url, self.filename))
        self.arguments[0] = path(self.filename).basename()
        image_node_list = Image.run(self)
        return image_node_list

    def get_tryton_main(self):
        if ViewDirective.tryton_main is not None:
            return ViewDirective.tryton_main

        config = self.state.document.settings.env.config
        proteus_instance = proteus.config._CONFIG.current
        ViewDirective._get_tryton_configuration(config, proteus_instance)

        # Open session in server
        # Now, it only works with local instances because it mixes RPC calls
        # and trytond module importation
        tryton.rpc.login(self.trytond_user,
            self.trytond_password,
            self.trytond_host,
            self.trytond_port,
            self.trytond_dbname)
        # TODO: put some wait because sometimes the login window is raised

        tryton_main = tryton.gui.Main(ViewDirective)
        ViewDirective.tryton_main = tryton_main

        tryton.common.ICONFACTORY.load_client_icons()

        tryton_main._width = self.tryton_default_width
        tryton_main._height = self.tryton_default_height
        tryton_main.window.set_default_size(tryton_main._width,
            tryton_main._height)
        tryton_main.window.resize(tryton_main._width, tryton_main._height)

        self._close_menu(tryton_main)
        self._login(tryton_main)
        return tryton_main

    @classmethod
    def _get_tryton_configuration(cls, config, proteus_instance):
        cls.trytond_host = config.trytond_host
        cls.trytond_port = (int(config.trytond_port) if config.trytond_port
            else None)
        cls.trytond_dbname = config.trytond_dbname
        cls.trytond_user = config.trytond_user
        cls.trytond_password = config.trytond_password
        cls.tryton_default_width = config.tryton_default_width
        cls.tryton_default_height = config.tryton_default_height


        if proteus_instance.config_file and (not cls.trytond_host or
                not cls.trytond_port):
            trytond_config = ConfigParser.ConfigParser()
            with open(proteus_instance.config_file, 'r') as f:
                trytond_config.readfp(f)
            if (trytond_config and
                    trytond_config.get('options', 'jsonrpc', False) and
                    len(trytond_config.get('options', 'jsonrpc').split(':'))
                        == 2):
                cls.trytond_host = (
                    trytond_config.get('options', 'jsonrpc').split(':')[0])
                cls.trytond_port = int(
                    trytond_config.get('options', 'jsonrpc').split(':')[1])

        if not cls.trytond_dbname and proteus_instance:
            cls.trytond_dbname = proteus_instance.database_name

    def _open_menu(self, tryton_main, menuitem_xml_id=None):
        if menuitem_xml_id is not None:
            module_name, fs_id = menuitem_xml_id.split('.')
            menuitem = get_ref_data(module_name, fs_id)
            if menuitem is None:
                sys.stderr.write("ERROR: view with XML ID '%s' doesn't "
                    "exists.\n" % menuitem_xml_id)
            else:
                selected_nodes = [menuitem.id]
                while menuitem.parent:
                    menuitem = menuitem.parent
                    selected_nodes.append(menuitem.id)

                selected_nodes.reverse()
                # Expanded nodes doesn't include the last item
                expanded_nodes = [selected_nodes[:-p-1]
                    for p in range(len(selected_nodes) - 1)]
                expanded_nodes.reverse()

                view = tryton_main.menu_screen.current_view
                view.expand_nodes(expanded_nodes)
                view.select_nodes([selected_nodes])
                tryton_main.menu_screen.save_tree_state()
                tryton_main.sig_win_menu(self.tryton_prefs)

        if not tryton_main.menu_expander.get_expanded():
            tryton_main.menu_toggle()

    def _close_menu(self, tryton_main):
        if tryton_main.menu_expander.get_expanded():
            tryton_main.menu_toggle()

    def _login(self, tryton_main):
        prefs = tryton.common.RPCExecute('model', 'res.user',
            'get_preferences', False)
        ViewDirective.tryton_prefs = prefs

        tryton.common.ICONFACTORY.load_icons()
        tryton.common.MODELACCESS.load_models()
        tryton.common.MODELHISTORY.load_history()
        tryton.common.VIEW_SEARCH.load_searches()

        if prefs and 'language_direction' in prefs:
            tryton.translate.set_language_direction(
                prefs['language_direction'])

        tryton_main.sig_win_menu(prefs=prefs)
        tryton_main.set_title(prefs.get('status_bar', ''))

        if prefs and 'language' in prefs:
            tryton.translate.setlang(prefs['language'], prefs.get('locale'))
            # if prefs['language'] != CONFIG['client.lang']
            tryton_main.set_menubar()
            tryton_main.favorite_unset()

        tryton_main.favorite_unset()
        tryton_main.menuitem_favorite.set_sensitive(True)
        tryton_main.menuitem_user.set_sensitive(True)
        return True

    @classmethod
    def force_quit(cls):
        try:
            tryton.rpc.logout()
            gtk.main_quit()
        except:
            pass

    def calc_url(self, view_xml_id, domain=None):
        module_name, fs_id = view_xml_id.split('.')
        view = get_ref_data(module_name, fs_id)
        if view is None:
            sys.stderr.write("ERROR: view with XML ID '%s' doesn't exists.\n"
                % view_xml_id)
            return ''
        domain_str = ('&domain=%s' % domain) if domain else ''
        return 'tryton://%s:%s/%s/model/%s;views=[%s]%s' % (self.trytond_host,
            self.trytond_port, self.trytond_dbname, view.model, view.id,
            domain_str)

    def screenshot(self, tryton_main, url, field_name):
        self._close_all_tabs(tryton_main)

        width = self.options.get('width', '').replace('px', '').strip()
        width = (int(width) if width and width.isdigit()
            else self.tryton_default_width)
        height = self.options.get('height', '').replace('px', '').strip()
        height = (int(height) if height and height.isdigit()
            else self.tryton_default_height)
        tryton_main.window.resize(width, height)

        tryton_main.open_url(url)

        if self.options.get('show_menu'):
            self._open_menu(tryton_main,
                menuitem_xml_id=self.options['show_menu'])
        else:
            self._close_menu(tryton_main)

        if field_name:
            gobject.timeout_add(2000, self.set_cursor, tryton_main, field_name)

        gobject.timeout_add(6000, self.draw_window, tryton_main.window)
        gtk.main()
        return True

    def _close_all_tabs(self, tryton_main):
        res = True
        while res:
            wid = tryton_main.get_page()
            if wid:
                for dialog in wid.dialogs[:]:
                    dialog.destroy()
                # wid.screen.save_tree_state()
                # wid.screen.current_view.set_value()
                res = tryton_main._win_del()
            else:
                res = False
        if tryton_main.menu_screen:
            # tryton_main.menu_screen.save_tree_state()
            tryton_main.menu_screen.destroy()
            tryton_main.menu_screen = None
        tryton_main.menu_expander_clear()
        tryton_main.sig_win_menu(prefs=self.tryton_prefs)
        return True

    def set_cursor(self, tryton_main, field_name):
        tryton_main.current_page = tryton_main.notebook.get_current_page()
        current_form = tryton_main.get_page(tryton_main.current_page)
        current_view = (current_form.screen.current_view
            if current_form and current_form.screen else None)
        if current_view and current_view.view_type in ('tree', 'form'):
            current_view.cursor_widget = field_name

            def _set_cursor():
                if (tryton_main.current_page
                        == tryton_main.notebook.get_current_page()):
                    current_view.set_cursor(reset_view=True)
            # Using idle_add because the gtk.TreeView grabs the focus at the
            # end of the event
            gobject.idle_add(_set_cursor)

    def draw_window(self, win):
        # Code below from:
        # http://stackoverflow.com/questions/7518376/creating-a-screenshot-of-a-gtk-window
        # More info here:
        # http://burtonini.com/computing/screenshot-tng.py

        width, height = win.get_size()
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width,
            height)

        # Retrieve the pixel data from the gdk.window attribute (win.window)
        # of the gtk.window object
        screenshot = pixbuf.get_from_drawable(win.window, win.get_colormap(),
            0, 0, 0, 0, width, height)

        screenshot.save(self.filename, 'png')
        gtk.main_quit()
        # Return False to stop the repeating interval
        return False


class References(Transform):
    """
    Parse and transform tryref and field references in a document.
    """

    default_priority = 999

    def apply(self):
        config = self.document.settings.env.config
        pattern = config.trydoc_pattern
        if isinstance(pattern, basestring):
            pattern = re.compile(pattern)
        for node in self.document.traverse(nodes.Text):
            parent = node.parent
            if isinstance(parent, (nodes.literal, nodes.FixedTextElement)):
                # ignore inline and block literal text
                continue
            text = unicode(node)
            modified = False

            match = pattern.search(text)
            while match:
                if len(match.groups()) != 1:
                    raise ValueError(
                        'trydoc_issue_pattern must have '
                        'exactly one group: {0!r}'.format(match.groups()))
                # extract the reference data (excluding the leading dash)
                refdata = match.group(1)
                start = match.start(0)
                end = match.end(0)

                data = refdata.split(':')
                kind = data[0]
                content = data[1]
                if len(data) > 2:
                    options = data[2]
                else:
                    options = None

                if kind == 'field':
                    model_name, field_name = content.split('/')
                    if options == 'help':
                        show_help = True
                    else:
                        show_help = False
                    replacement = get_field_data(model_name, field_name,
                        show_help)
                elif kind == 'tryref':
                    ref, field = content.split('/')
                    module_name, fs_id = ref.split('.')
                    replacement = get_ref_data(module_name, fs_id, field)
                else:
                    replacement = refdata

                text = text[:start] + replacement + text[end:]
                modified = True

                match = pattern.search(text)

            if modified:
                parent.replace(node, [nodes.Text(text)])


def init_transformer(app):
    if app.config.trydoc_plaintext:
        app.add_transform(References)
    if (app.config.trydoc_modules and
            proteus.config._CONFIG.current.database_name == ':memory:'):
        module_model = proteus.Model.get('ir.module.module')
        modules_to_install = []
        for module_to_install in app.config.trydoc_modules:
            res = module_model.find([('name', '=', module_to_install)])
            # if app.config.verbose:
            sys.stderr.write("INFO: Module found with name '%s': %s.\n"
                    % (module_to_install, res))
            if res:
                modules_to_install.append(res[0].id)
        if modules_to_install:
            proteus_context = proteus.config._CONFIG.current.context
            # if app.config.verbose:
            sys.stderr.write("INFO: It will install the next modules: %s with "
                    "context %s.\n" % (modules_to_install,
                                proteus_context))
            module_model.install(modules_to_install, proteus_context)
        proteus.Wizard('ir.module.module.install_upgrade').execute('upgrade')


def remove_temporary_files(app, exception):
    ViewDirective.force_quit()
    for filename in screenshot_files:
        if os.path.exists(filename):
            os.remove(filename)


def setup(app):
    app.add_config_value('trydoc_plaintext', True, 'env')
    app.add_config_value('trydoc_pattern', re.compile(r'@(.|[^@]+)@'), 'env')
    app.add_config_value('trydoc_modelclass', 'trydocmodel', 'env')
    app.add_config_value('trydoc_fieldclass', 'trydocfield', 'env')
    app.add_config_value('trydoc_refclass', 'trydocref', 'env')
    app.add_config_value('trydoc_viewclass', 'trydocview', 'env')
    app.add_config_value('trydoc_modules', [], 'env')
    app.add_config_value('trytond_host', 'localhost', 'env')
    app.add_config_value('trytond_port', 8000, 'env')
    app.add_config_value('trytond_dbname', None, 'env')
    app.add_config_value('trytond_user', 'admin', 'env')
    app.add_config_value('trytond_password', 'admin', 'env')
    app.add_config_value('tryton_default_width', 2048, 'env')
    app.add_config_value('tryton_default_height', 1024, 'env')
    # app.add_config_value('verbose', False, 'env'),

    app.add_directive('model', ModelDirective)
    app.add_directive('field', FieldDirective)
    app.add_directive('tryref', TryRefDirective)
    app.add_directive('view', ViewDirective)

    app.connect(b'builder-inited', init_transformer)
    app.connect(b'build-finished', remove_temporary_files)
