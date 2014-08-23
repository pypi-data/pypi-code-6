# Django imports
from django.conf.urls import patterns, include, url


from djhcup_integration.views import index


# base patterns always available through having djhcup_core installed
urlpatterns = patterns('',
    url(r'$', index, name='int_index'),
)