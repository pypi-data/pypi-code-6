#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from datetime import datetime
import pytz
from siegfried import get_simple_domain, prepare_url
import feedparser
from HTMLParser import HTMLParser

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

# check google alerts links.
re_ga_link = re.compile(r'http(s)?://www\.google\.com/url\?q=')

# domains to ignore
BAD_DOMAINS = [
  'pastpages',
  'twitter',
  'inagist'
]

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

def parse_date(entry):

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

def parse_authors(entry):
  # TODO, add in author parsing
  return entry.author

def parse_id(entry):
  return entry.id.split(':')[-1]

def parse_entry(entry):
  return {
    'galert_id': parse_id(entry),
    'url': parse_link(entry),
    'title': parse_title(entry),
    'summary': parse_summary(entry),
    'datetime': parse_date(entry)
  }

def parse_galerts_feed(**kw):
  
  feed = kw.get('feed')

  # user feedparser
  f = feedparser.parse(feed)

  # step through links, check for bad domains
  for entry in f.entries:
    url = parse_link(entry)
    if get_simple_domain(url) not in BAD_DOMAINS:
      yield parse_entry(entry)

from gnulynx import GnuTask

class GoogleAlertsFeed(GnuTask):
  
  def main(self, **kw):
    return parse_galerts_feed(**kw)

if __name__ == '__main__':
  f = GoogleAlertsFeed()
  f.cli()
