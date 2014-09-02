import logging

from django import forms
from djblets.siteconfig.forms import SiteSettingsForm
from reviewboard.accounts.backends import AuthBackend

from .providers import accounts


# XXX Create OAuthServiceAccount and OAuthService classes

class OAuthSettingsForm(SiteSettingsForm):
    
    class Meta:
        title = 'OAuth Backend Settings'


class OAuthBackend(AuthBackend):
    backend_id = 'oauth'
    name = 'OAuth'  # Displayed/used in admin interface.
    supports_registration = False

    login_instructions = 'Leave these blank (use an OAuth button below).'

    def authenticate(self, username, password):
        try:
            provider, account = accounts.extract_provider_and_account(password,
                                                                      username)
        except Exception as e:
            logging.debug('authentication failure: {}'.format(e))
            return None
        else:
            if account is None:
                logging.debug('account not found: {!r}'.format(username))
                return None

            actual = accounts.authenticate(provider, account)
            if actual is None:
                return None
            return accounts.get_or_create_user(actual.username)

    def get_or_create_user(self, username, request):
        token = request.GET.get('token', request.POST.get('token'))
        if token is None:
            return None
        # XXX Finish!
        raise NotImplementedError
        return accounts.get_or_create_user(account.username)


def add_provider_settings(provider):
    # XXX How to make use of these settings?

    if provider.APP_ID_FIELD is None:
        return
    
    try:
        form = OAuthBackend.settings_form
    except AttributeError:
        form = None
    if form is None:
        settings_form = OAuthSettingsForm

    # XXX Group the provider's fields in the form.

    # Add the app's provider-registered ID.
    name = 'auth_oauth_app_id_' + provider.NAME.lower(),
    field = forms.CharField(label=provider.APP_ID_FIELD,
                            help_text=provider.APP_ID_HELP,
                            required=True,
                            )
    setattr(OAuthSettingsForm, name, field)

    # Add the app's secret key (given by provider), if applicable.
    if provider.APP_SECRET_FIELD is None:
        name = 'auth_oauth_app_secret_' + provider.NAME.lower(),
        field = forms.CharField(label=provider.APP_SECRET_FIELD,
                                help_text=provider.APP_SECRET_HELP,
                                required=True,
                                )
        setattr(OAuthSettingsForm, name, field)
