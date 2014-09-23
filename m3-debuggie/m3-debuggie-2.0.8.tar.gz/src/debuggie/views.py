# -*- coding: utf-8 -*-

from django.shortcuts import (
    render_to_response, HttpResponseRedirect,
)
from django.core.urlresolvers import reverse

import api

def debug_status(request):
    """
    Вывод текущего состояния логгера
    """
    if request.user.is_authenticated():
        return render_to_response(
            'debug_status.html',
            {
                'status': api.get_status(request),
                'download_url': api.get_download_url(request),
            }
        )
    else:
        return render_to_response('unauthenticated.html')

def debug_toggle(request):
    """
    Переключение состояния логгера
    """
    if request.user.is_authenticated():
        api.toggle_status(request)
    return HttpResponseRedirect(reverse(debug_status))


def debug_clear(request):
    """
    Очистка списка событий
    """
    if request.user.is_authenticated():
        api.clear_records(request)
    return HttpResponseRedirect(reverse(debug_status))
