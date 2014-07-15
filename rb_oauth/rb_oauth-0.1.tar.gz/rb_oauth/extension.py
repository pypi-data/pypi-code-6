"""A reviewboard extension that provides OAuth authentication.

The extension could be used to authenticate against any OAuth provider,
though for now it is just set up for github.

Each provider should have a button added to templates/providers.html and
should have a provider.Provider subclass registered (using
register_provider).

"""
from django.conf import settings
from django.conf.urls import patterns, include, url

# XXX This is just a temporary hack allowing us to import this
# module in setup.py.
try:
    settings.configure()
except Exception:
    pass
from reviewboard.extensions.base import Extension


class OAuthExtension(Extension):

    is_configurable = False

    #default_settings = {'createuser': True,
    #                    'createaltusername': False,
    #                    'disablepassword': True,
    #                    }

    def initialize(self):
        from . import defaults as _  # Imported only for side-effects.

        from djblets.extensions.hooks import TemplateHook
        TemplateHook(self, 'after-login-form', 'providers.html')

        from reviewboard.extensions.hooks import URLHook
        exturl = url(r'^oauth/', include('rb_oauth.urls'))
        toplevel = patterns('', exturl)
        URLHook(self, toplevel)

        from reviewboard.extensions.hooks import AuthBackendHook
        from ._backend import OAuthBackend
        AuthBackendHook(self, OAuthBackend)
