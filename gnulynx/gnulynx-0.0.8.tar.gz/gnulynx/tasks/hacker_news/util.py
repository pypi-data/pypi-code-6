from datetime import datetime
import pytz 
import requests
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