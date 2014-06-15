"""
Dashboard
=========

utility to register a dashboard to be used when creating the *main* project
dashboard. This dashboard needs to be a DashboardGroup

.. note::

   Note that the application dashboard is registered via a different mechanism, 
   i.e.: the registration of admin_tools. That register function needs a 
   DashboardAppIndex class. Both are registered within app'``dashboars.py`` 
   that will be read only if ``urs.py`` starts an autodiscovery:

      import admin_tools.dashboard
      admin_tools.dashboard.autodiscover()

registry
--------

Info are kept in a dict named registry than can be accessed to loop on 
registered applications::

  from jmb.core.adm import dashboard
  for appname, dash in dashboard.registry.iteritems():
      ...

The whole dahboard machinery is fired from the variables:

:ADMIN_TOOLS_DASHMOARD: whose default is set as ``../dashboard.JumboDashboard`` 
            by ``jmb-start`` skel
:ADMIN_TOOLS_MENU: whose default is set as ``../menu.JumboMenu`` by ``jmb-start`` 
            skel

.. note::

   the menu is triggered from a templatetag withing ``admin/base_site.html``


It's up to aplication authors to correctly set it up, so that out default 
``dashboard.py``, present in out Skeleton will find and display it. 

.. autofunction:: register_group

.. autofunction:: unregister_group

.. autofunction:: get_group

"""
from admin_tools.dashboard  import modules

registry = {}

def register_group(group, app_name):
    """Register a :class:`admin_tools.dashboard.modules.Group` group to be 

    :param app_name: the application name, e.g.: jmb.fax
    :param group: an instance of a :class:`modules.Group`. It can also be 
    """
    msg = "group must be DashboardModule or Group, found %s" 
    assert issubclass(group, modules.DashboardModule), msg % group
    registry[app_name] = group

def unregister_group(app_name):
    """Unregister a :class:`admin_tools.dashboard.modules.Group` group to be  

    :param app_name: the application name, e.g.: jmb.fax
    """
    del registry[app_name] 

def get_group(app_name):
    """return a :class:`modules.Group` for app_name or None
    
    :param app_name: the application name, e.g.: jmb.fax
    """
    return registry.get(app_name, None)


    
