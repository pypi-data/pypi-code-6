from django.conf.urls import url
from fandjango.decorators import facebook_authorization_required as fb_auth
from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.http import urlencode
from functools import wraps
from response import *
from messaging import *
from django_websocket.decorators import websocket


def fb_auth_ajax(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.facebook and request.facebook.user:
            return view(request, *args, **kwargs)
        else:
            return JSONResponse({'errors': 'Must fully authorize the application'}, status=403)
    return wrapper


class CookieSafeFBEntryPointError(Exception): pass


class CookieSafeFBEntryPoint(object):

    def __init__(self, base_path, page='', permissions=[]):
        """
        Crea un punto de entrada para una aplicacion de
        Facebook. Por ahora bancamos puntos de entrada de
        aplicacion o de tab. despues vemos de bancar mas.
 
        :param page:
        :param permissions:
        :param base_path: path base (en django) que sirve todo
            este entry point
        :return:
        """

        if not page:
            self.istab = False
            self.baseurl = "http://apps.facebook.com/%s/" % settings.FACEBOOK_APPLICATION_NAMESPACE
        else:
            self.istab = True
            self.baseurl = "https://www.facebook.com/%s/app_%s" % (page, settings.FACEBOOK_APPLICATION_ID)
        self.permissions = permissions
        self.base_path = base_path

    def _make_facebook_url(self, request):
        """
        Devuelve una url transformada a la
        correspondiente url de facebook.
        """
        path = request.path #ej. /path/to/fbapp/my/url
        base_path = self.base_path.rstrip('/') #ej. /path/to/fbapp
        if not path.startswith(base_path):
            raise CookieSafeFBEntryPointError("URL %s is not child of %s" % (path, self.base_path))
        return self.baseurl.rstrip('/') + path[len(base_path):] if not self.istab else self.baseurl

    @staticmethod
    def firsthand_cookie_view(request):
        """
        Crea la cookie de primera mano para
        que luego pueda ser editada.
        """
        response = HttpResponse(content="""
<html>
    <body>
        <script type="text/javascript">
            window.top.location.href = %s;
        </script>
    </body>
</html>
""" % json.dumps(request.GET.get("back", "http://www.facebook.com")))
        response.set_cookie(getattr(settings, 'FACEBOOK_ENTRYPOINT_PUT_1ST_COOKIE_NAME', 'safari_sucks'), True)
        return response

    @staticmethod
    def firsthand_cookie_url(pattern):
        """
        Crea la entrada de URL para la url de la vista que pone la cookie inicial.
        """
        return url(pattern,
                   CookieSafeFBEntryPoint.firsthand_cookie_view,
                   name=settings.FACEBOOK_ENTRYPOINT_PUT_1ST_COOKIE_URL)

    def fb_entry_point(self):
        """
        Genera dinamicamente un decorador que, tomando la vista, arma
        una vista decorada por el facebook_authorization_required con
        los parametros seleccionados desde los atributos de esta clase.
        :param args:
        :param kwargs:
        :return:
        """

        def _is_firsthand_cookie(view):
            def wrapped(request, *args, **kwargs):
                if not request.COOKIES.get(getattr(settings, 'FACEBOOK_ENTRYPOINT_PUT_1ST_COOKIE_NAME', 'safari_sucks'), False):
                    target = settings.FANDJANGO_SITE_URL.rstrip('/') + resolve_url(settings.FACEBOOK_ENTRYPOINT_PUT_1ST_COOKIE_URL)
                    current = self._make_facebook_url(request)
                    template = """
<html>
    <body>
        <script type="text/javascript">
            window.top.location.href = %s;
        </script>
    </body>
</html>
""" % (json.dumps(target + '?' + urlencode({'back': current})))
                    return HttpResponse(content=template)
                else:
                    return view(request, *args, **kwargs)
            return wrapped

        def decorator(view):
            return wraps(view)(
                fb_auth(redirect_uri=self.baseurl, permissions=self.permissions)(
                    _is_firsthand_cookie(
                        view
                    )
                )
            )
        return decorator

    def fb_ajax_entry_point(self):
        """
        Es igual a fb_entry_point PERO con json/ajax. La otra diferencia es que
        esta no puede llenar cookies, ya que es solamente json.
        :param args:
        :param kwargs:
        :return:
        """
        return fb_auth_ajax

    def fb_websocket_entry_point(self):
        """
        Es igual a fb_entry_point PERO con websockets. La otra diferencia es que
        esta no puede llenar cookies, ya que es una peticion websockets.
        """
        def decorator(view):
            @websocket
            def wrapped(request, ws, *args, **kwargs):
                if request.facebook and request.facebook.user:
                    return view(request, ws, *args, **kwargs)
                else:
                    ws.close(4003, "You must fully authorize the application")
            return wrapped
        return decorator

    def authorized_url(self, pattern, view, name=None, kwargs={}, urltype=None):
        """
        Crea la entrada de URL para esta vista en particular.
        """
        trimmed_bp = self.base_path.strip('/')
        trimmed_pt = pattern.lstrip('^/')
        if urltype == 'ajax':
            decorator = self.fb_ajax_entry_point()
        elif urltype == 'websocket':
            decorator = self.fb_websocket_entry_point()
        else:
            decorator = self.fb_entry_point()
        return url('^%s/%s' % (trimmed_bp, trimmed_pt), decorator(view), kwargs, name)
