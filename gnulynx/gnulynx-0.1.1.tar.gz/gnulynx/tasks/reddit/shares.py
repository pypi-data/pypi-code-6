#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnulynx import GnuTask
from gnulynx.util import utc_now
from gnulynx.serialize import from_json

import re
import requests
from requests import ConnectionError

endpoint = 'http://buttons.reddit.com/button_info.json'

class RedditShares(GnuTask):

  def main(self, **kw):
    
    url = kw.get('url')

    params = {
      'url': url,
      'format': 'json',
    }
    headers = {
      'User-Agent': self.opts['user_agent']
    } 
    
    try:
      r = requests.get(endpoint, params=params, headers=headers)
    
    except ConnectionError as e:
      self.log.error(e)
    
    else:
      yield r.json()

if __name__ == '__main__':
  f = RedditShares()
  f.cli()
