import datetime

import lauteur
from siegfried import (
  prepare_url, urls_from_html, is_article_url
  )

from libs import feedparser
from util import (
  get_jsonpath, strip_tags, parse_datetime, imgs_from_html
  )


# JSONPATH CANDIDATES
URL_CANDIDATE_JSONPATH = [
  'id', 'feedburner_origlink', 'link', 'links[*].href'
]

# applies to feed AND individual entries.
DATE_CANDIDATE_JSONPATH = [
  'updated_parsed', 'published_parse'
]

AUTHOR_CANDIDATE_JSONPATH = [
  'author', 'author_detail.name', 'authors[*].name'
]

IMG_CANDIDATE_JSONPATH = [
  'media_content[*].url'
]

CONTENT_CANDIDATE_JSONPATH = [
  'content[*].value', 'summary'
]

TAG_CANDIDATE_JSONPATH = [
  'tags[*].label', 'tags[*].term'
]


# MAIN CLASS
class SupeRSSInitError(Exception):
  pass

class SupeRSS:
  """
  Strategy: 
  """
  
  def __init__(self, feed, **kwargs):

    # required kwargs
    self.feed            = feed
    self.is_full_text    = kwargs.get('is_full_text', True)


  def get_candidates(self, obj, jsonpath):
    """
    evaluate an object with jsonpath, 
    and get all unique vals / lists
    of values
    """
    candidates = set()
    for path in jsonpath:
      path_candidates = get_jsonpath(obj, path)

      if isinstance(path_candidates, list):
        for candidate in path_candidates:
          if candidate:
            candidates.add(candidate)

      elif isinstance(path_candidates, str):
        candidates.add(candidate)

    return list(candidates)


  def get_datetime(self, obj):
    """
    return earliest time of candidates or current time.
    """
    candidates = self.get_candidates(obj, DATE_CANDIDATE_JSONPATH)
    if len(candidates) > 0:
      return parse_datetime(sorted(candidates)[0])
    else:
      return datetime.utcnow()


  # get authors, using `lauteur` for parsing.
  def get_authors(self, entry):
    """
    return all candidates, and parse unique
    """
    
    authors = set()
    
    _authors = self.get_candidates(entry, AUTHOR_CANDIDATE_JSONPATH)
    for _a in _authors:
      for author in lauteur.from_string(_a):
        authors.add(author)

    return list(authors)


  # get images
  def get_imgs(self, entry):
    """

    """
    img_urls = self.get_candidates(entry, IMG_CANDIDATE_JSONPATH)
    return list(set(img_urls))
  

  def get_article_html(self, entry):
    """
    Get all article text candidates and check which one is the longest.
    """
    candidates = self.get_candidates(entry, CONTENT_CANDIDATE_JSONPATH)
    candidates.sort(key = len)
    return candidates[-1]
  

  def get_tags(self, entry):
    tags = self.get_candidates(entry, TAG_CANDIDATE_JSONPATH)
    return list(set(tags))


  def get_url(self, entry):
    """
    Two strategies:
    1: check candidates for valid urls
    2: Open / Unshorten candidates
    3: If still none, default to first candidate
    """
    # defaults to orig_link -> id -> link
    # only if valid
    if 'feedburner_origlink' in entry: 
      if is_article_url(entry.feedburner_origlink):
        return prepare_url(entry.feedburner_origlink)
  
    if 'link' in entry:
      if is_article_url(entry.link):
        return prepare_url(entry.link)

    if 'id' in entry:
      if is_article_url(entry.id):                  
        return prepare_url(entry.id)

    # get potential candidates
    candidates = self.get_candidates(entry, URL_CANDIDATE_JSONPATH)

    # if no candidates, return an empty string
    if len(candidates) == 0:
      #print "< no url found! >"
      return None

    # test for valid urls:
    articles_urls = list(set([
      u for u in candidates if is_article_url(u)
      ]))
    
    # if we have one or more, update entry_urls and return the first
    if len(articles_urls) >= 1:
      return valid_urls[0]

    # if we STILL haven't found anything, just
    # return the first candidate:
    return candidates[0]


  def get_links(self, article_html):
    return [prepare_url(u) for u in urls_from_html(article_html)]


  def parse_entry(self, entry):

    """
    Parse an entry. if not full text, extract the article
    by opening the page and merge the results.
    """
    article_html = self.get_article_html( entry )

    data = {
      'url':           self.get_url(entry),
      'article_html':  article_html,
      'text':          strip_tags(article_html),
      'title':         entry.title,
      'tags':          self.get_tags(entry),
      'authors':       self.get_authors(entry),
      'datetime':      self.get_datetime(entry),
      'img_urls':      self.get_imgs(article_html),
      'article_links': self.get_links(article_html),
      'article_imgs':  imgs_from_html(article_html)
    }

    return data


  def run(self):
    """
    parse feed and stream entries
    """
    f = feedparser.parse(self.feed)

    # go latest to earliest, so when
    # we check for duplicates we get them first.
    entries = reversed(f.entries)
    for entry in f.entries:
      data = self.parse_entry(entry)
      if self.is_full_text:
        yield data 

      else:
        # TODO article extraction and merging!
        pass

