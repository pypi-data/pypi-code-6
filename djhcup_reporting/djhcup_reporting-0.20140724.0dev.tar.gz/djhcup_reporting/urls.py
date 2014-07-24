# Django imports
from django.conf.urls import patterns, include, url


from djhcup_reporting.views import index, query_builder, dataset_details


# base patterns always available through having djhcup_core installed
urlpatterns = patterns('',
    url(r'new/$', query_builder, name='query_builder'),
    #url(r'new/(?P<universe_pk>\d+)/$', query_builder_filters, name='query_builder_choose_filters'),
    url(r'dataset/(?P<dataset_dbo_name>[_a-z0-9]+)/$', dataset_details, name='dataset_details'),
    url(r'$', index, name='rpt_index')
)