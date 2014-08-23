# Django imports
from django.conf.urls import patterns, include, url


from djhcup_reporting.views import index, query_builder, dataset_details, download_archive, universe_details, datasets_browse


# base patterns always available through having djhcup_core installed
urlpatterns = patterns('',
    url(r'new/$', query_builder, name='query_builder'),
    url(r'universe/(?P<universe_pk>\d+)/$', universe_details, name='universe_details'),
    url(r'dataset/$', datasets_browse, name='datasets_browse'),
    url(r'dataset/(?P<dataset_dbo_name>[_a-z0-9]+)/download/$', download_archive, name='download_archive'),
    url(r'dataset/(?P<dataset_dbo_name>[_a-z0-9]+)/$', dataset_details, name='dataset_details'),
    url(r'$', index, name='rpt_index')
)