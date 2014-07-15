#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnulynx import GnuTask
from siegfried import prepare_url, urls_from_html

from util import hn_api, parse_time

class HackerNewsSearchPosts(GnuTask):

  def parse_post(self, s):
    return {
      'hn_id': s.get('objectID'),
      'author': s.get('author'),
      'title': s.get('title'),
      'url': prepare_url(s.get('url', '')),
      'datetime': parse_time(s.get('created_at_i'))
    } 

  def parse_posts(self, results):
    posts = results['hits']
    for post in posts:
      yield parse_post(post)

  def search_hn_posts(self, **kw):
    query = kw.get('query')
    pages = kw.get('pages', 1)
    for page in range(0, pages):
      
      try:
        posts = hn_api(query, tags='story', page=page)
      
      except Exception as e:
        self.log.error(e)
      
      else:
        for post in parse_posts(posts):
          yield post
  
  def main(self, **kw):
    return self.search_hn_posts(
      query = kw.get('query'),
      **self.opts
      )

if __name__ == '__main__':
  f = HackerNewsSearchPosts()
  f.cli()
