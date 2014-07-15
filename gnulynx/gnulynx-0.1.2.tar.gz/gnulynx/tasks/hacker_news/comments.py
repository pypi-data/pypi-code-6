#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnulynx import GnuTask

from siegfried import prepare_url, urls_from_html

from util import hn_api, parse_time, strip_tags


class HackerNewsSearchComments(GnuTask):

  def parse_comment(self, s):
    return {
      'hn_id': s.get('objectID'),
      'author': s.get('author', ''),
      'title': s.get('title'),
      'urls': [prepare_url(u) for u in urls_from_html(s.get('comment_text', ''))],
      'datetime': parse_time(s.get('created_at_i')),
      'comment': strip_tags(s.get('comment_text', ''))
    }

  def parse_comments(self, results):
    comments = results['hits']
    for comment in comments:
      yield parse_comment(comment)
  
  def search_hn_comments(self, **kw):
    query = kw.get('query')
    pages = kw.get('pages', 1)
    for page in range(0, pages):
      try:
        comments = hn_api(query, tags='comment', page=page)
      except Exception as e:
        self.log.error(e)
      else:
        for comment in parse_comments(comments):
          yield comment

  def main(self, **kw):
    return self.search_hn_comments(
      query = kw.get('query'),
      **self.opts
      )

if __name__ == '__main__':
  f = HackerNewsSearchComments()
  f.cli()
