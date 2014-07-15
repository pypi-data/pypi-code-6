#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnulynx import GnuTask
from gnulynx.util import utc_now

import requests
from requests import ConnectionError

endpoint = 'http://www.linkedin.com/countserv/count/share'

class LinkedInShares(GnuTask):

  def main(self, **kw):
    url = kw.get('url')
    params = {
      'format': 'json',
      'url': url
    }
    
    try:
      r = requests.get(endpoint, params=params)

    except ConnectionError as e:
      self.log.error(e)
      
    else:
      data = r.json()
      yield {
        'url' : url,
        'datetime': utc_now(),
        'count': data['count']
      }

if __name__ == '__main__':
  f = LinkedInShares()
  f.cli()