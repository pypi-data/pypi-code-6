# -*- coding: utf-8 -*-

import re
import json
from base64 import b64decode as decode

from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.conf import settings
from studiogdo.api import StudiogdoApi


class SkelView(TemplateView):
    template_name = 'studiogdo/skel.html'

    @property
    def data(self):
        if not hasattr(self, "_data"):
            self._data = getattr(self.request, self.request.method)
        return self._data

    def get_entry(self, **kwargs):
        return kwargs['entry']

    def get_skel(self):
        return self.data.get('m')

    def get_facet(self):
        return self.data.get('f')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if settings.STUDIOGDO_FACET == "django":
            entry = self.get_entry(**kwargs)
            facet = self.get_facet()

            # django facet entry is not done on java
            if entry == "facet" and facet == StudiogdoApi.DEFAULT_MODE:
                entry = "empty"

            # should be optimized to be called only if needed
            api = request.studiogdo_api
            response = api.send(request.method.lower(), '%s.gdo' % entry, self.data)

            # on error 412 return error message
            if response.status_code == 412:
                valid = re.compile(r"<b>message</b> <u>([^<]*)</u>")
                se = valid.search(response.content)
                return HttpResponse(status=412, content=se.groups(0))

            content = response.content
            if response.status_code == 200:

                # django facet are rendered by django
                if facet == StudiogdoApi.DEFAULT_MODE:
                    if not hasattr(self, 'skel'):
                        self.skel = self.get_skel()
                    skel = self.get(request, *args, **kwargs)
                    ap = self.data.get('ap')
                    renderer = request.html_renderer
                    content = renderer.render(decode(ap) if ap else "/", skel.render().content.decode('utf-8'))

                # if it'a a facet, we add a new attribute to the response
                elif facet == 'json' and response.content:
                    response.json = json.loads(response.content)
                elif facet == 'dom5':
                    response.html = response.content

            # create django response
            content_type = response.headers[
                'content-type'] if 'content-type' in response.headers else 'text/html; charset=utf-8'
            resp = HttpResponse(content=content, content_type=content_type,
                                status=response.status_code, reason=response.reason)

            for header, value in response.headers.iteritems():
                # if header in ['content-length', 'content-disposition']:
                if header in ['content-disposition']:
                    resp[header] = value

        elif settings.STUDIOGDO_FACET == "java":
            # if the request has a facet, get it as a template
            if self.data.get('f', None) == StudiogdoApi.DEFAULT_MODE:
                self.skel = self.get_skel()
                skel = self.get(request, *args, **kwargs)
                self.data['m'] = skel.render().content
                # check if skel extension is jskel for json or skel to html facet
                self.data['f'] = 'json' if self.skel.endswith("jskel") else 'dom5'

            api = request.studiogdo_api
            entry = self.get_entry(**kwargs)
            response = api.send(request.method.lower(), '%s.gdo' % entry, self.data)

            # on error 412 return error message
            if response.status_code == 412:
                valid = re.compile(r"<b>message</b> <u>([^<]*)</u>")
                se = valid.search(response.content)
                return HttpResponse(status=412, content=se.groups(0))

            if response.status_code == 200:

                # if it'a a facet, we add a new attribute to the response
                facet_mode = self.data.get('f', "")
                if facet_mode == 'json' and response.content:
                    response.json = json.loads(response.content)
                elif facet_mode == 'dom5':
                    response.html = response.content

            # create django response
            content_type = response.headers[
                'content-type'] if 'content-type' in response.headers else 'text/html; charset=utf-8'
            resp = HttpResponse(content=response.content, content_type=content_type,
                                status=response.status_code, reason=response.reason)

            for header, value in response.headers.iteritems():
                # if header in ['content-length', 'content-disposition']:
                if header in ['content-disposition']:
                    resp[header] = value

        return resp


class PIPView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # check connected
        api = request.studiogdo_api
        response = api.post_facet(None, '<span data-path="/Session/User(1)"></span>', "dom5")
        facet = unicode(response.content, 'utf-8')
        if not facet:
            data = {}
            data["param1"] = request.user.username
            api.apply_command("/", "Connect", data)

        return super(PIPView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return 'pip/' + self.template_name


class LoginView(TemplateView):
    template_name = 'pip/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                api = request.studiogdo_api
                data = {}
                data["param1"] = username
                api.apply_command("/", "Connect", data)
                redirect_to = request.GET.get('next', reverse('accueil'))
                return redirect(redirect_to)
            else:
                msg = "Vous avez été déconnecté..."
        else:
            msg = "Paramètres de connexion invalides!"
        c = {}
        c["error_msg"] = msg
        c.update(csrf(request))
        return render_to_response(LoginView.template_name, c)

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        api = request.studiogdo_api
        api.disconnect()
        return super(LoginView, self).get(request, *args, **kwargs)


class AccueilView(PIPView):
    template_name = 'accueil.html'
    pip = {}

    def get_context_data(self, *args, **kwargs):
        context = super(AccueilView, self).get_context_data(*args, **kwargs)
        context['pip'] = AccueilView.pip

class LockView(PIPView):
    pass


class UnlockView(PIPView):
    pass
