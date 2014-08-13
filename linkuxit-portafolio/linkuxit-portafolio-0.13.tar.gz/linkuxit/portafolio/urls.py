from django.conf.urls import patterns, url

urlpatterns = patterns(
    'linkuxit.portafolio.views',

    # Main details
    url(r'^member/(?P<slug>[-\w]+)/$', 'member_detail', name="linkuxit_portafolio_member_detail"),
    url(r'^project/(?P<slug>[-\w]+)/$', 'project_detail', name="linkuxit_portafolio_project_detail"),
    url(r'^team/(?P<slug>[-\w]+)/$', 'team_detail', name="linkuxit_portafolio_team_detail"),
    url(r'^service/(?P<slug>[-\w]+)/$', 'service_detail', name="linkuxit_portafolio_service_detail"),
    url(r'^client/(?P<slug>[-\w]+)/$', 'client_detail', name="linkuxit_portafolio_client_detail"),

    # list views
    url(r'^projects/$', 'project_list', name="linkuxit_portafolio_project_list"),
    url(r'^services/$', 'service_list', name="linkuxit_portafolio_service_list"),
    url(r'^teams/$', 'team_list', name="linkuxit_portafolio_team_list"),
    url(r'^clients/$', 'client_list', name="linkuxit_portafolio_client_list"),
)