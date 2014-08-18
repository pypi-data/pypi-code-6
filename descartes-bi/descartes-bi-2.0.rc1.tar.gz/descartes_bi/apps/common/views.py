import logging
import os

from django import http
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader
from django.views.generic import TemplateView

from dashboards.views import DashboardListView

logger = logging.getLogger(__name__)


def set_language(request):
    if request.method == 'GET':
        request.session['django_language'] = request.GET.get('language', 'en')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class HomeView(DashboardListView):
    pass


class AboutView(TemplateView):
    template_name = 'core/about.html'
