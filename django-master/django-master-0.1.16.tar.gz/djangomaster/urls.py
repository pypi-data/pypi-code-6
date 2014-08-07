from django.conf.urls import patterns, url, include

from djangomaster.views.home import HomeView
from djangomaster.views.routes import RoutesListView
from djangomaster.views.settings import SettingsListView
from djangomaster.views.lint import PyLintView, JsLintView


urlpatterns = patterns(r'',

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^routes/$', RoutesListView.as_view(), name='routes'),
    url(r'^settings/$', SettingsListView.as_view(), name='settings'),
    url(r'^pylint/$', PyLintView.as_view(), name='pylint'),
    url(r'^jslint/$', JsLintView.as_view(), name='jslint'),

)

