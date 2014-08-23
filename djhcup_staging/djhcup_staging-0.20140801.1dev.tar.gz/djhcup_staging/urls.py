# Django imports
from django.conf.urls import patterns, include, url


from djhcup_staging.views import obj_detail, obj_inventory, index, run_batch, batch_from_unprocessed, create_batch_from_unimported, file_discover, file_match
#from djhcup_staging.views import file_detail, file_discover, file_match, file_inventory
#from djhcup_staging.views import ibatch_detail


# base patterns always available through having djhcup_core installed
ds_patterns = patterns('',
    url(r'(?P<obj_id>\d+)/$', obj_detail, {'obj_type': 'DataSource'}, name='ds_detail'),
    url(r'$', obj_inventory, {'obj_type': 'DataSource'}, name='ds_inv'),
)

file_patterns = patterns('',
    url(r'(?P<obj_id>\d+)/$', obj_detail, {'obj_type': 'File'}, name='file_detail'),
    url(r'(?P<year>\d+|all)/(?P<state_abbr>[A-Z]{2}|all)/$', obj_inventory, {'obj_type': 'File'}, name='file_inv'),
    url(r'discover/$', file_discover),
    url(r'match/$', file_match),
    url(r'$', obj_inventory, {'obj_type': 'File'}, name='file_inv'),
)

ibatch_patterns = patterns('',
    url(r'(?P<obj_id>\d+)/$', obj_detail, {'obj_type': 'ImportBatch'}, name='imb_detail'),
    url(r'(?P<obj_id>\d+)/run/$', run_batch, {'obj_type': 'ImportBatch'}, name='imb_run'),
    url(r'unimported_batch/$', create_batch_from_unimported),
    url(r'$', obj_inventory, {'obj_type': 'ImportBatch'}, name='imb_inv'),
)

stbatch_patterns = patterns('',
    url(r'(?P<obj_id>\d+)/$', obj_detail, {'obj_type': 'StagingBatch'}, name='stb_detail'),
    url(r'(?P<obj_id>\d+)/run/$', run_batch, {'obj_type': 'StagingBatch'}, name='stb_run'),
    url(r'unprocessed_batch/$', batch_from_unprocessed),
    url(r'$', obj_inventory, {'obj_type': 'StagingBatch'}, name='stb_inv'),
)

tbl_patterns = patterns('',
    url(r'(?P<obj_id>\d+)/$', obj_detail, {'obj_type': 'StagingTable'}, name='tbl_detail'),
    #url(r'(?P<year>\d+|all)/(?P<state_abbr>[A-Z]{2}|all)/$', obj_inventory, {'obj_type': 'StagingTable'}, name='tbl_inv'),
    #url(r'(?P<category>[A-Z_]+|all)/(?P<year>[0-9]{4}|all)/(?P<state_abbr>[A-Z]{2}|all)/$',
    url(r'(?P<year>[0-9]{4}|all)/(?P<state_abbr>[A-Z]{2}|all)/$',
        obj_inventory,
        {'obj_type': 'StagingTable'},
        name='tbl-inventory-filtered'
        ),
    url(r'$', obj_inventory, {'obj_type': 'StagingTable'}, name='tbl_inv'),
)

col_patterns = patterns('',
    url(r'(?P<obj_id>\d+)/$', obj_detail, {'obj_type': 'Column'}), # links to the state-year and table each is from
    url(r'name/(?P<name>\S+)/$', obj_inventory, {'obj_type': 'Column'}, name='col_inv'), # shows the state-year and table each is from
)


urlpatterns = patterns('',
    url(r'data_sources/', include(ds_patterns)),
    url(r'files/', include(file_patterns)),
    url(r'imports/', include(ibatch_patterns)),
    url(r'staging/', include(stbatch_patterns)),
    url(r'tables/', include(tbl_patterns)),
    url(r'columns/', include(col_patterns)),
    url(r'$', index, name='stg_index'),
)

# source_populate_defaults
