#################################
#
# Thread local settings storage
#
# Fork on https://djangosnippets.org/snippets/1945/
#
# Use threading.local() to store thread
# specific settings
#
# Reads from threading.local first and
# from settings as a fall-back
#

from django.conf import settings
import threading


DISABLE_LOGGING = True

if not DISABLE_LOGGING and settings.DEBUG:
    import logging


class LocalSettings():
    """
    Singleton interface to threading.local() settings override
    """
    __instance = None

    def __init__(self):
        if LocalSettings.__instance is None:
            if not DISABLE_LOGGING and settings.DEBUG:
                logging.warn('LocalSettings : CREATE SINGLETON')

            LocalSettings.__instance = threading.local()
            # Store __instance reference as the only member in the handle
            self.__dict__['_LocalSettings__instance'] = LocalSettings.__instance

    def __getattr__(self, key):
        if not DISABLE_LOGGING and settings.DEBUG :
            logging.warn('%s LocalSettings : GET key %s - thread %s' % (getattr(LocalSettings.__instance, 'SITE_ID', getattr(settings, 'SITE_ID')), key, threading.currentThread()))
        try:
            return getattr(LocalSettings.__instance, key)
        except:
            return getattr(settings, key)

    def __setattr__(self, key, value):
        if not DISABLE_LOGGING and settings.DEBUG:
            logging.warn('%s LocalSettings : SET %s = %s - thread %s' % (getattr(LocalSettings.__instance, 'SITE_ID', getattr(settings, 'SITE_ID')), key, value , threading.currentThread()))
        setattr(LocalSettings.__instance, key, value)

localsettings = LocalSettings()



def load_settings_from(file_name):
    pass
