from django.conf.urls import patterns, url

from djangomaster.views.home import HomeView
from djangomaster.views.routes import RoutesListView
from djangomaster.views.settings import SettingsListView
from djangomaster.views.signals import SignalsListView
from djangomaster.views.lint import PyLintView, JsLintView
from djangomaster.views.test import TestView, ExecuteTestView, CheckTestView
from djangomaster.views.south import SouthView


urlpatterns = patterns(
    r'',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^routes/$', RoutesListView.as_view(), name='routes'),
    url(r'^settings/$', SettingsListView.as_view(), name='settings'),
    url(r'^pylint/$', PyLintView.as_view(), name='pylint'),
    url(r'^jslint/$', JsLintView.as_view(), name='jslint'),
    url(r'^signals/$', SignalsListView.as_view(), name='signals'),
    url(r'^south/$', SouthView.as_view(), name='south'),

    # Tests
    url(r'^test/$', TestView.as_view(), name='test'),
    url(r'^test/execute/$', ExecuteTestView.as_view(), name='test_execute'),
    url(r'^test/check/$', CheckTestView.as_view(), name='test_check'),
)
