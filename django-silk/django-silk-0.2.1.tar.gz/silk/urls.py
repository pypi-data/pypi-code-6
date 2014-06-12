from django.conf.urls import patterns, url

from silk.views.profile_detail import ProfilingDetailView
from silk.views.profiling import ProfilingView
from silk.views.raw import Raw
from silk.views.request_detail import RequestView
from silk.views.root import RootView
from silk.views.sql import SQLView
from silk.views.sql_detail import SQLDetailView


urlpatterns = patterns('silk.views',
                       url(r'^/$', RootView.as_view(), name='requests'),
                       url(r'^/request/(?P<request_id>[0-9]+)/$', RequestView.as_view(), name='request_detail'),
                       url(r'^/request/(?P<request_id>[0-9]+)/sql/$', SQLView.as_view(), name='request_sql'),
                       url(r'^/request/(?P<request_id>[0-9]+)/sql/(?P<sql_id>[0-9]+)/$', SQLDetailView.as_view(), name='request_sql_detail'),
                       url(r'^/request/(?P<request_id>[0-9]+)/raw/$', Raw.as_view(), name='raw'),
                       url(r'^/request/(?P<request_id>[0-9]+)/profiling/$', ProfilingView.as_view(), name='request_profiling'),
                       url(r'^/request/(?P<request_id>[0-9]+)/profile/(?P<profile_id>[0-9]+)/$', ProfilingDetailView.as_view(), name='request_profile_detail'),
                       url(r'^/request/(?P<request_id>[0-9]+)/profile/(?P<profile_id>[0-9]+)/sql/$', SQLView.as_view(), name='request_and_profile_sql'),
                       url(r'^/request/(?P<request_id>[0-9]+)/profile/(?P<profile_id>[0-9]+)/sql/(?P<sql_id>[0-9]+)/$', SQLDetailView.as_view(), name='request_and_profile_sql_detail'),
                       url(r'^/profile/(?P<profile_id>[0-9]+)/$', ProfilingDetailView.as_view(), name='profile_detail'),
                       url(r'^/profile/(?P<profile_id>[0-9]+)/sql/$', SQLView.as_view(), name='profile_sql'),
                       url(r'^/profile/(?P<profile_id>[0-9]+)/sql/(?P<sql_id>[0-9]+)/$', SQLDetailView.as_view(), name='profile_sql_detail'),
                       url(r'^/profiling/$', ProfilingView.as_view(), name='profiling'))


