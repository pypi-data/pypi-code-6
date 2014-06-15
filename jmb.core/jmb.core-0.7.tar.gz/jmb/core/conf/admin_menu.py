from admin_tools.menu import items, Menu

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.db.models import get_model

from jmb.core.middleware.thread_local import get_current_user

class GenericMenuItem:
    def __init__(self, app_name, models_menu):
        self.app_name = app_name
        self.models_menu = models_menu
        self.menu_complete = []
        self.user = get_current_user()
        self.dchildren = {}
        self.has_permissions = False
        self.create_menu()

    def get_menu(self):
        return self.menu_complete

    def create_menu(self):
        for model in self.models_menu:
            if self.user.has_perm("%s.view_%s" % (self.app_name, model)): # or user.has_perm("organization.view_contact"):
                verbose_name_plural = get_model(self.app_name, model)._meta.verbose_name_plural.capitalize()
                menuitems = items.MenuItem(
                    title=verbose_name_plural,
                    children=self.get_generic_menu(model),
                    url = reverse('admin:%s_%s_changelist' % (self.app_name, model))
                )
                self.menu_complete.append(menuitems)
                self.dchildren[model] = menuitems


    def get_generic_menu(self, model):
        child_menu = []

        # LIST PERMISSION
        if self.user.has_perm("%s.view_%s" % (self.app_name, model)):
            verbose_name_plural = get_model(self.app_name, model)._meta.verbose_name_plural.capitalize()
            child_menu.append(items.MenuItem(
                title=_('List %s') % verbose_name_plural,
                children=[],
                url = reverse('admin:%s_%s_changelist' % (self.app_name, model))
            ))

        # ADD PERMISSION
        if self.user.has_perm("%s.add_%s" % (self.app_name, model)):
            verbose_name = get_model(self.app_name, model)._meta.verbose_name.capitalize()
            child_menu.append(items.MenuItem(
                title=_('Add %s') % verbose_name,
                children=[],
                url = reverse('admin:%s_%s_add' % (self.app_name, model))
            ))

        return child_menu


    def add_child(self, child, model, position=None):
        if self.dchildren.has_key(model):
            if position == 0 or position:
                self.dchildren[model].children.insert(position, child)
            else:
                self.dchildren[model].children.append(child)


    def add_father(self, child, position=None):
        #if check_permission and not self.menu_complete:
        #    return None

        if position == 0 or position:
            self.menu_complete.insert(position, child)
        else:
            self.menu_complete.append(child)
