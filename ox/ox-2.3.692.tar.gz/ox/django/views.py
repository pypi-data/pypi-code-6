# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from six import StringIO, PY2
from six.moves import urllib
from six.moves import http_cookiejar as cookielib

from celery.utils import get_full_cls_name
from celery.backends import default_backend

from django.http import HttpResponse
from django.conf import settings

from shortcuts import json_response
import ox


def task_status(request, task_id):
    response = json_response(status=200, text='ok')
    status = default_backend.get_status(task_id)
    res = default_backend.get_result(task_id)
    response['data'] = {
        'id':     task_id,
        'status': status,
        'result': res
    }
    if status in default_backend.EXCEPTION_STATES:
        traceback = default_backend.get_traceback(task_id)
        response['data'].update({'result':    str(res.args[0]),
                                 'exc':       get_full_cls_name(res.__class__),
                                 'traceback': traceback})
    return response

class SessionCookieJar(cookielib.LWPCookieJar):
    def save(self):
        return "#LWP-Cookies-2.0\n" + self.as_lwp_str()

    def load(self, data, ignore_discard=True, ignore_expires=True):
        f = StringIO(data)
        self._really_load(f, 'memory', ignore_discard, ignore_expires)

def api_proxy(request):
    '''
        settings.OXAPI_URL =...
        from ox.django.views import api_proxy
        urlpatterns = patterns('',
            url(r'^api/$', api_proxy)
    '''
    url = settings.OXAPI_URL
    cj = SessionCookieJar()
    if 'cj' in request.session:
        cj.load(request.session['cj'])
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [
        ('User-Agent', request.META.get('HTTP_USER_AGENT'))
    ]
    form = ox.MultiPartForm()
    for key in request.POST:
        form.add_field(key, request.POST[key])
    r = urllib.request.Request(url)
    body = form.body()
    r.add_header('Content-type', form.get_content_type())
    r.add_header('Content-length', len(body))
    r.add_data(body)
    f = opener.open(r)
    response = HttpResponse(f.read())
    request.session['cj'] = cj.save()
    return response
