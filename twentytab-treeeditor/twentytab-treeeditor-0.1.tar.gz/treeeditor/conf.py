from appconf import AppConf
from django.conf import settings


class TreeEditorConf(AppConf):
    STATIC_URL = u'/static/'
    TREE_EDITOR_INCLUDE_ANCESTORS = False
    TREE_EDITOR_OBJECT_PERMISSIONS = False
    JQUERY_LIB = u"{}{}".format(u'/static/', u"treeeditor/js/jquery-2.1.0.min.js")
    JQUERYUI_LIB = u"{}{}".format(u'/static/', u"treeeditor/js/jquery-ui-1.10.4.custom.min.js")
    JQUERYUI_CSSLIB = u"{}{}".format(u'/static/', u"treeeditor/css/smoothness/jquery-ui-1.10.4.custom.min.css")

    def configure_static_url(self, value):
        if not getattr(settings, 'STATIC_URL', None):
            self._meta.holder.STATIC_URL = value
            return value
        return getattr(settings, 'STATIC_URL')

    def configure_tree_editor_include_ancestors(self, value):
        if not getattr(settings, 'TREE_EDITOR_INCLUDE_ANCESTORS', None):
            self._meta.holder.TREE_EDITOR_INCLUDE_ANCESTORS = value
            return value
        return getattr(settings, 'TREE_EDITOR_INCLUDE_ANCESTORS')

    def configure_tree_editor_object_permissions(self, value):
        if not hasattr(settings, 'TREE_EDITOR_OBJECT_PERMISSIONS'):
            self._meta.holder.TREE_EDITOR_OBJECT_PERMISSIONS = value
            return value
        return getattr(settings, 'TREE_EDITOR_OBJECT_PERMISSIONS')

    def configure_jquery_lib(self, value):
        if not getattr(settings, 'JQUERY_LIB', None):
            self._meta.holder.JQUERY_LIB = value
            return value
        return getattr(settings, 'JQUERY_LIB')

    def configure_jqueryui_lib(self, value):
        if not getattr(settings, 'JQUERYUI_LIB', None):
            self._meta.holder.JQUERYUI_LIB = value
            return value
        return getattr(settings, 'JQUERYUI_LIB')

    def configure_jqueryui_csslib(self, value):
        if not getattr(settings, 'JQUERYUI_CSSLIB', None):
            self._meta.holder.JQUERYUI_CSSLIB = value
            return value
        return getattr(settings, 'JQUERYUI_CSSLIB')