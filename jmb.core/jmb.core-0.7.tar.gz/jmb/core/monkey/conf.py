"""
.. _jquery_cms:

Django and jQuery
==================

.. autofunction:: patch_cms_page_not_to_overwrite_jquery

"""

def patch_cms_page_not_to_overwrite_jquery():
    """MonkeyPatch django-cms not to overwrite jquery.

    While django make attention to use djangojQuery and not to overwite
    standard $(), so different versions can coexist, PageAdmin and
    PluginEditor overwrite it with ``django.jQuery``. Utilizzata in urls.py
    cosi::

      from jmb.core import monkey

      if settings.CMS_ENABLED:
          urlpatterns += patterns('',
              url(r'^', include('cms.urls')),
          )
          monkey.patch_cms_page_not_to_overwrite_jquery()

    """
    from cms.utils import cms_static_url
    from cms.admin import pageadmin
    from cms.forms import widgets

    pageadmin.PageAdmin.Media.js = [
        cms_static_url(path) for path in [
            'js/libs/jquery.query.js',
            'js/libs/jquery.ui.dialog.js',
        ]
    ]
    
    widgets.PluginEditor.Media.js = [
        cms_static_url(path) for path in [
            'js/plugin_editor.js',
        ]
    ]
    
