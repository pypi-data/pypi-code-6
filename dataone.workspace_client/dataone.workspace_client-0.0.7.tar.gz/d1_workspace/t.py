#!/usr/bin/env python

import logging
import time

import workspace_solr_client

logging.basicConfig()


options = {
  'base_url': 'https://cn.dataone.org/cn',
  'solr_query_timeout': 30.0,
  'max_objects_for_query': 50,
}

c = workspace_solr_client.SolrClient(options)

query = u'id:{0}'.format('123')

time.sleep(60 * 10)

c.query(query)
c.query(query)
