from praw import Reddit
from siegfried import prepare_url
from datetime import datetime
import pytz 

def parse_time(utc_ts):
  return datetime.fromtimestamp(utc_ts, tz=pytz.utc)

def parse_result(s):
  return {
    'datetime': parse_time(s.created_utc),
    'summary': s.title,
    'reddit_id': s.id,
    'url': prepare_url(s.url),
    'reddit_url': s.permalink,
    'author': s.author.name 
  }

def reddit_search(query, sort="new", user_agent = "NewsLynx"):
  r = Reddit(user_agent = user_agent)
  results = r.search(query, sort=sort)
  for result in results:
    yield parse_result(result)

from gnulynx import GnuTask

class RedditSearch(GnuTask):

  def main(self, **kw):
    return reddit_search(
      query = kq.get('query')
      **self.opts
      )

if __name__ == '__main__':
  f = RedditSearch()
  f.cli()
