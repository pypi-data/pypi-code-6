from django.conf.urls import url, patterns
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'django_idshost.views',
    url(r'^logout_ids/', 'logout_ids',
        name='ids_disconnect'),
    url(r'^logout/', 'logout', name='logout'),
)
