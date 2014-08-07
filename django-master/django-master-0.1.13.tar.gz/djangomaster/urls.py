from django.conf.urls import patterns, url, include

from djangomaster.views.home import HomeView
from djangomaster.views.routes import RoutesListView
from djangomaster.views.settings import SettingsListView


urlpatterns = patterns(r'',

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^routes/$', RoutesListView.as_view(), name='routes'),
    url(r'^settings/$', SettingsListView.as_view(), name='settings'),

)

