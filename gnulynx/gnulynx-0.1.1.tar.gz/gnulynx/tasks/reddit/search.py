#!/usr/bin/env python
# -*- coding: utf-8 -*-

from praw import Reddit
from praw.handlers import MultiprocessHandler

from siegfried import prepare_url, urls_from_html
from datetime import datetime
import pytz 
from HTMLParser import HTMLParser

def unescape(htmlentities):
  if htmlentities:
    h = HTMLParser()
    return h.unescape(htmlentities)
  else:
    return ''

def parse_time(utc_ts):
  return datetime.fromtimestamp(utc_ts, tz=pytz.utc)

def parse_result(s):
  return {
    'datetime': parse_time(s.created_utc),
    'title': s.title,
    'text': s.selftext,
    'urls': list(set([prepare_url(u) for u in urls_from_html(unescape(s.selftext_html))])),
    'reddit_id': s.id,
    'reddit_url': s.permalink,
    'author': s.author.name 
  }

def reddit_search(query, sort="new", user_agent = "GnuLynx", multiprocess=True):
  
  if multiprocess:
    handler = MultiprocessHandler()
    r = Reddit(user_agent = user_agent, handler=handler)

  else:
    r = Reddit(user_agent = user_agent)

  for result in r.search(query, sort=sort):
    yield parse_result(result)

from gnulynx import GnuTask

class RedditSearch(GnuTask):

  def main(self, **kw):
    return reddit_search(**dict(kw.items() + self.opts.items()))

if __name__ == '__main__':
  r = RedditSearch()
  r.cli()
