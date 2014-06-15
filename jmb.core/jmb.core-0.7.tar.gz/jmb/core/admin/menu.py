"""
Menu
=========

utility to register a menu to be used when creating the main project
menu. Menu will be rendered by a templatedtab named admin_tools_render_menu 
that is present in ``jmb.core:admin/base_site.html`` menu. Be sure not to 
hide it in project's templates.

Info are kept in a dict named registry than can be accessed to loop on 
registered applications::

  from jmb.core.adm import menu
  for appname, dash in dashboard.registry.iteritems():
      ...


.. autofunction:: register_menu

.. autofunction:: unregister_menu

"""
from admin_tools.menu import items, Menu

registry = {}

def register_menu(menu_item, app_name):
    """Register a :class:`admin_tools.dashboard.modules.Group` group to be 

    :param app_name: the application name, e.g.: jmb.fax
    :param group: an instance of a :class:`modules.Group`. It can also be 
    """
    msg = "group must be MenuItem, found %s" 
    assert isinstance(menu_item, items.MenuItem), msg % menu_item
    registry[app_name] = menu_item

def unregister_menu(app_name):
    """Unregister a :class:`admin_tools.dashboard.modules.Group` group to be 

    :param app_name: the application name, e.g.: jmb.fax
    """
    del registry[app_name] 



    
