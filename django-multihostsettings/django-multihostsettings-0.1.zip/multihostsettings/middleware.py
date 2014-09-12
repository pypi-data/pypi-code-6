from . import localsettings
from django.contrib.sites.models import Site
import importlib


class MultiHostSettingsMiddleware(object):
    """ Change Settings dynamically with thread local settings storage """

    def process_request(self, request):
        domain = request.get_host()
        if domain not in localsettings.MULTIHOST_SETTINGS:
            return None
            
        file_name = localsettings.MULTIHOST_SETTINGS[domain]

        try:
            settings = importlib.import_module(file_name)

            for setting in dir(settings):
                if not setting.startswith('_'):
                    value = getattr(settings, setting)
                    setattr(localsettings, setting, value)
        except:
            pass

        return None
