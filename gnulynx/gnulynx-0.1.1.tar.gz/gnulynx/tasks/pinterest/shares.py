#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnulynx import GnuTask
from gnulynx.util import utc_now
from gnulynx.serialize import from_json

import re
import requests
from requests import ConnectionError

endpoint = 'http://api.pinterest.com/v1/urls/count.json?url='
re_callback = re.compile(r'^receiveCount\((.*)\)$')

class PinterestShares(GnuTask):

  def main(self, **kw):
    url = kw.get('url')

    try:
      r = requests.get(endpoint + url)
    
    except ConnectionError as e:
      self.log.error(e)
    
    else:
      # pinterest only does jsonp, so we'll parse out the callback function
      raw = r.content
      m = re_callback.search(raw)
      if m:
        data = from_json(m.group(1))
        data['datetime'] = utc_now()
        yield data 
      
if __name__ == '__main__':
  f = PinterestShares()
  f.cli()