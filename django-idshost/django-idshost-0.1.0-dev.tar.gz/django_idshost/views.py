from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.views import logout as main_logout
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.conf import settings

from spyne.server.django import DjangoApplication
from spyne.server.wsgi import WsgiApplication
from spyne.model.primitive import String, Boolean, Unicode, Integer
from spyne.model.complex import Iterable
from spyne.service import ServiceBase
from spyne.protocol.soap import Soap11
from spyne.application import Application
from spyne.decorator import rpc
from spyne.interface.wsdl import Wsdl11


SETTINGS = getattr(settings, 'DJANGO_IDSHOST_SETTINGS', {})

if not SETTINGS.get('APP_NAME') or not SETTINGS.get('PRIVATE_IP'):
    raise Exception("You have to init the django_idshost settings to use"
                    " this app. Read the doc.")
else:
    app = SETTINGS.get('APP_NAME')
    private_ip = SETTINGS.get('PRIVATE_IP')
    public_url = SETTINGS.get('PUBLIC_URL', 'http://{app}'.format(app=app))


class AuthIds(ServiceBase):

    @rpc(String, String, String, _out_variable_name='IsValid',
         _returns=Boolean)
    def CheckPassword(ctx, OrganizationUnit, Authentifier, Password):
        res = False
        user = get_user_model().objects.get(username=Authentifier[2:])
        if user and user.check_password(Password):
            res = True
        return res


_app = Application([AuthIds],
                   '{public_url}'.format(public_url=public_url),
                   in_protocol=Soap11(validator='lxml'),
                   out_protocol=Soap11(),
                   name='idscheckpasswordservice',

                   )

_django_app = DjangoApplication(_app)
_django_app.doc.wsdl11.build_interface_document(
    "http://{private}/CheckPassword/".format(private=private_ip)
)

django_app = csrf_exempt(_django_app)


def _logout_url(request, next_page):

    protocol = 'https://'
    host = request.META.get('HTTP_HOST')
    url = protocol + host + next_page
    return url


def logout(request, **kwargs):
    if request.COOKIES.get('sessionids'):
        next_page = _logout_url(request, reverse('ids_disconnect'))
    else:
        prot = 'https://' if request.is_secure() else 'http://'
        next_page = prot + request.META.get('HTTP_HOST')
    return main_logout(request, next_page=next_page, **kwargs)


def logout_ids(request, **kwargs):
    return render(request, 'api/logout_ids.html',
                  {'auth': request.user.ids_authentifier})
