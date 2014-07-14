#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnulynx import GnuTask
from gnulynx.util import utc_now

import requests
from requests import ConnectionError

endpoint = "http://urls.api.twitter.com/1/urls/count.json?url="

class TwitterShares(GnuTask):

  def main(self, **kw):
    url = kw.get('url')
    
    try:
      r = requests.get(endpoint + url)
    
    except ConnectionError as e:
      self.log.error(e)

    else:
      data = r.json()
      data['datetime'] = utc_now()
      yield data

if __name__ == '__main__':
  f = TwitterShares()
  f.cli()