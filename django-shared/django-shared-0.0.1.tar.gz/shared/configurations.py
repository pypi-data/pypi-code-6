class ExternalCredentials:
    """
    Mixin for a Configuration class of django-configurations.
    Enables one to load specific variables from <myproject>/configs/<DJANGO_CONFIGURATION>.py
    Good to separate critical information from the settings itself.
    """

    @staticmethod
    def get_credentials_module():
        """
        Returns the credentials module.

        :returns: the module
        :rtype: module
        """
        import inspect
        import importlib
        import os

        return importlib.import_module(
            '%(module)s.configs.%(stage)s' % {
                # inspect the stack and get the calling module (<myproject>.settings)
                'module': inspect.getmodule(inspect.stack()[1][0]).__name__.split('.')[0],
                'stage': os.environ['DJANGO_CONFIGURATION']
            }
        )
