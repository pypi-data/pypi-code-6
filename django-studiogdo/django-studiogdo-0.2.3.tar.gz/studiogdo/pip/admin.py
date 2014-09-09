# -*- coding: utf-8 -*-
from base64 import b64encode

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.module_loading import import_by_path
from django.utils.functional import LazyObject


class PipAdmin(object):
    menu = {}
    accueil_tabs = {}

    def __init__(self):
        """
        verify menu dictionnary
        """
        self.complete_menu()
        self.complete_accueil_tabs()

    def complete_menu(self):
        for group, menu_group in self.menu.iteritems():
            for item in menu_group:
                flags = {'label': 'label' in item}
                if False in flags.values():
                    raise ValidationError('flag %s missing' % str(flags))

                # default url value (if not sub menu)
                if not 'url' in item and not 'menu' in item:
                    item['url'] = item['label'].lower()

                if 'path' in item:
                    item['path'] = b64encode(item['path'])

                for sub_menu in item.get('menu', []):
                    if 'path' in sub_menu:
                        sub_menu['path'] = b64encode(sub_menu['path'])
            else:
                if group != group.lower():
                    menu_group = self.menu.pop(group)
                    self.menu[group.lower()] = menu_group

    def complete_accueil_tabs(self):
        for group in self.accueil_tabs.iterkeys():
            if group != group.lower():
                    menu_group = self.accueil_tabs.pop(group)
                    self.accueil_tabs[group.lower()] = menu_group


class ConfiguredStorage(LazyObject):
    def _setup(self):
        self._wrapped = import_by_path("pip.admin.%s" % settings.PIP_ADMIN)()

admin = ConfiguredStorage()
