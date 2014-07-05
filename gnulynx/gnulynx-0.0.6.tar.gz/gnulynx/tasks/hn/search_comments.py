
from datetime import datetime
import pytz 
import requests
from siegfried import prepare_url, urls_from_html
from HTMLParser import HTMLParser
import re

hn_search_endpoint = 'http://hn.algolia.com/api/v1/search_by_date'

def parse_time(utc_ts):
  return datetime.fromtimestamp(utc_ts, tz=pytz.utc)

# html stripping
class MLStripper(HTMLParser):
  def __init__(self):
    self.reset()
    self.fed = []

  def handle_data(self, d):
    self.fed.append(d)

  def get_data(self):
    return ''.join(self.fed)

def strip_tags(html):
  """
  string tags and clean text from html.
  """
  s = MLStripper()
  s.feed(html)
  raw_text = s.get_data()
  raw_text = re.sub(r'\n|\t|\r', ' ', raw_text)
  return re.sub('\s+', ' ', raw_text).strip()

def hn_api(query, tags, page=0):
  params = {
    'query': query,
    'tags': tags,
    'page': page,
  }
  r = requests.get(hn_search_endpoint, params=params)
  return r.json()

def parse_comment(s):
  return {
    'hn_id': s.get('objectID'),
    'author': s.get('author', ''),
    'title': s.get('title'),
    'urls': [prepare_url(u) for u in urls_from_html(s.get('comment_text', ''))],
    'datetime': parse_time(s.get('created_at_i')),
    'comment': strip_tags(s.get('comment_text', ''))
  }

def parse_comments(results):
  comments = results['hits']
  for comment in comments:
    yield parse_comment(comment)

def search_hn_comments(**kw):
  query = kw.get('query')
  pages = kw.get('pages', 1)
  for page in range(0, pages):
    comments = hn_api(query, tags='comment', page=page)
    for comment in parse_comments(comments):
      yield comment

from gnulynx import GnuTask

class HackerNewsSearchComments(GnuTask):
  
  def main(self, **kw):
    return search_hn_comments(
      query = kw.get('query'),
      **self.opts
      )

if __name__ == '__main__':
  f = HackerNewsSearchComments()
  f.cli()
