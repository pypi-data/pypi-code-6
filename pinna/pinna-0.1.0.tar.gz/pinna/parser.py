#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from HTMLParser import HTMLParser
import time
from datetime import datetime
import pytz

from siegfried import get_simple_domain, prepare_url

from libs import feedparser

# check google alerts links.
re_ga_link = re.compile(r'http(s)?://www\.google\.com/url\?q=')

# domains to ignore
BAD_DOMAINS = [
  'pastpages',
  'twitter',
  'inagist'
]

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

def time_to_datetime(ts):
  """
  convert time to datetime obj
  """
  return datetime.fromtimestamp(time.mktime(ts))

# HELPERS # 
def parse_link(entry):
  raw_link = re_ga_link.sub('', entry.link)
  if '&ct=ga' in raw_link:
    raw_link = raw_link.split('&ct=ga')[0]
  return prepare_url(raw_link)

def parse_title(entry):
  return strip_tags(entry.title)

def parse_summary(entry):
  return strip_tags(entry.summary)

def parse_date(entry, set_as_now):

  if set_as_now:
    t = entry.published_parsed
    return datetime(
      year = t.tm_year,
      month = t.tm_mon,
      day = t.tm_mday,
      hour = t.tm_hour,
      minute = t.tm_min,
      second = t.tm_sec,
      tzinfo = pytz.utc
      )
    return time_to_datetime()
  else:
    return datetime.utcnow()

def parse_authors(entry):
  # TODO, add in author parsing
  return entry.author

def parse_id(entry):
  return entry.id.split(':')[-1]

def parse_entry(entry, set_as_now):
  data = {}
  data['galert_id'] = parse_id(entry)
  data['url'] = parse_link(entry)
  data['title'] = parse_title(entry)
  data['summary'] = parse_summary(entry)
  data['datetime'] = parse_date(entry, set_as_now)
  return data

def get_alerts(feed_url, **kwargs):
  
  # set as now T/F
  set_as_now = kwargs.get('set_as_now', True) 

  # user feedparser
  f = feedparser.parse(feed_url)

  # step through links, check for bad domains
  for entry in f.entries:
    url = parse_link(entry)
    if get_simple_domain(url) not in BAD_DOMAINS:
      yield parse_entry(entry, set_as_now)

if __name__ == '__main__':
  feed_url = 'http://www.google.com/alerts/feeds/14752688329844321840/4874425503898649357'
  for item in get_alerts(feed_url):
    print item

