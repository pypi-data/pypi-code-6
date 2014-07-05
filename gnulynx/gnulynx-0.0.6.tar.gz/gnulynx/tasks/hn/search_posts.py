from datetime import datetime
import pytz 
import requests
from siegfried import prepare_url, urls_from_html

hn_search_endpoint = 'http://hn.algolia.com/api/v1/search_by_date'

def parse_time(utc_ts):
  return datetime.fromtimestamp(utc_ts, tz=pytz.utc)

def hn_api(query, tags, page=0):
  params = {
    'query': query,
    'tags': tags,
    'page': page,
  }
  r = requests.get(hn_search_endpoint, params=params)
  return r.json()

def parse_post(s):
  return {
    'hn_id': s.get('objectID'),
    'author': s.get('author'),
    'title': s.get('title'),
    'url': prepare_url(s.get('url', '')),
    'datetime': parse_time(s.get('created_at_i'))
  } 

def parse_posts(results):
  posts = results['hits']
  for post in posts:
    yield parse_post(post)

def search_hn_posts(**kw):
  query = kw.get('query')
  pages = kw.get('pages', 1)
  for page in range(0, pages):
    posts = hn_api(query, tags='story', page=page)
    for post in parse_posts(posts):
      yield post

from gnulynx import GnuTask

class HackerNewsSearchPosts(GnuTask):
  
  def main(self, **kw):
    return search_hn_posts(
      query = kw.get('query'),
      **self.opts
      )

if __name__ == '__main__':
  f = HackerNewsSearchPosts()
  f.cli()
