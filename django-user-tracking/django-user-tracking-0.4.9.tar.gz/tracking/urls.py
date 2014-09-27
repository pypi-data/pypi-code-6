from django.conf.urls import patterns, include, url

from tracking.views import update_active_users, get_active_users, display_map
# from tracking import settings

urlpatterns = patterns(
    '',
    url(r'^refresh/$', update_active_users, name='refresh'),
    url(r'^refresh/json/$', get_active_users, name='get'),
)

# if getattr(settings, 'TRACKING_USE_GEOIP', False):
#    urlpatterns += patterns(
#        '',
#        url(r'^map/$', display_map, name='tracking-visitor-map'),
#    )
