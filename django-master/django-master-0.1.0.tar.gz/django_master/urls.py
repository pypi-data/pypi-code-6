from django.conf.urls import patterns, url

from django_master.views.routes import RoutesListView
from django_master.views.settings import SettingsListView

urlpatterns = patterns(r'',

    url(r'^routes/$', RoutesListView.as_view(), name="routes"),
    url(r'^settings/$', SettingsListView.as_view(), name="settings"),

)
