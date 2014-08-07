from django.conf.urls import patterns, url, include

from djangomaster.views.home import HomeView
from djangomaster.views.routes import RoutesListView
from djangomaster.views.settings import SettingsListView
from djangomaster.views.lint import LintView


urlpatterns = patterns(r'',

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^routes/$', RoutesListView.as_view(), name='routes'),
    url(r'^settings/$', SettingsListView.as_view(), name='settings'),
    url(r'^lint/$', LintView.as_view(), name='lint'),

)

