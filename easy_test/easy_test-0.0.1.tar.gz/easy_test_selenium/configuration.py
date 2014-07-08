# configuration.py use the user's settings and replace it with global setting
from importlib import import_module
import os

class Settings():
    def __init__(self):
        self.ENVIRONMENT_VARIABLE = "EASY_TEST_SETTINGS"
        self.settings_module = os.environ.get(self.ENVIRONMENT_VARIABLE)

    def getConfiguration(self):
        ENVIRONMENT_VARIABLE = "EASY_TEST_SETTINGS"

        # Get setting definition
        settings_module = self.settings_module
        if not settings_module:
            raise Exception("You need to configure an enviroment in manage.py")

        # Import setting definition
        try:
            mod = import_module(settings_module)
        except ImportError as e:
            raise ImportError(
                "Could not import settings '%s' (Is it on sys.path? Is there an import error in the settings file?): %s"
                % (settings_module, e)
            )
        return mod




