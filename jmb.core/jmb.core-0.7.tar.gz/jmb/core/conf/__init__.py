"""
Default settings
================


All default setting must be set in a module called 'settings' inside the
application. Application's ``__init__.py`` must contain the lines::

  from jmb.core.conf import inject_app_defaults

  inject_app_defaults(__name__)


So that all variables (*UPPER CASE ONLY*) get copied to settings singleton.

NOTE: in order to make this all work the module must not have been imported
      before the settings module. This means we should put ``tsettings`` out
      of the module to be sure it will work for applications

.. autofunction:: inject_app_defaults

"""
from jmb.core.monkey.conf import patch_cms_page_not_to_overwrite_jquery


def inject_app_defaults(application):
    """Inject an application's default settings

    :param application: the application whose settings must be injected. E.g: ``jmb.fax``
    """
    # https://github.com/thsutton/django-application-settings

    # importante per garantire che sys.module abbia global_settings
    from django.conf import global_settings
    try:
        __import__('%s.settings' % application)
        import sys
        
        # Import our defaults, project defaults, and project settings
        _app_settings = sys.modules['%s.settings' % application]
        _def_settings = sys.modules['django.conf.global_settings']
        _settings = sys.modules['django.conf'].settings

        # Add the values from the application.settings module
        for _k in dir(_app_settings):
            if _k.isupper():
                # Add the value to the default settings module
                setattr(_def_settings, _k, getattr(_app_settings, _k))

                # Add the value to the settings, if not already present
                if not hasattr(_settings, _k):
#                    _settings
                    setattr(_settings, _k, getattr(_app_settings, _k))

    except ImportError, e:
        # Silently skip failing settings modules
        pass

def set_interactive_user(username='admin'):
    """Implementa ThreadUser anche da shell interattiva::

         from jumbo import conf
         conf.set_interactive_user()
       
    """
    from django.conf import settings
    from django.contrib.auth.models import User
    setattr(settings, 'INTERACTIVE_USER', User.objects.get(username=username))


