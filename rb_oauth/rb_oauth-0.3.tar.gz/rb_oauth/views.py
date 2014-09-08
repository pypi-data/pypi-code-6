import urllib

from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from . import providers
from .providers import accounts


def oauth(request):
    # The django view for <reviewboard_root>/oauth/.

    if request.method == 'POST':
        resp = _handle_local_redirect(request)
    elif request.method == 'GET':
        resp = _handle_provider_redirect(request)
    else:
        raise NotImplementedError

    return resp


def _handle_local_redirect(request):
    # The local redirect to kick off the OAuth dance.
    callback = request.build_absolute_uri()
    provider = providers.extract_provider(request.POST, callback)
    resp = provider.initiate()
    return resp


def _handle_provider_redirect(request):
    # The response back from the provider with the valet key.
    provider = providers.extract_provider(request.GET)

    account = provider.handle(request.GET)
    if account is None:
        user = None
    else:
        username = account.username
        password = accounts.encode_password(provider.id)
        user = authenticate(username=username, password=password)
    if user is None:
        # XXX Use a proper auth failed response.
        resp = HttpResponseRedirect(reverse('login'))
    else:
        login(request, user)
        next = request.GET['next']
        if not next:
            next = '/dashboard/'
        resp = HttpResponseRedirect(next)

    return resp
