from gnulynx import GnuTask 
from gnulynx.util import utc_now 
from gnulynx.cli_util import write_stdout

import requests 
from requests import ConnectionError

class FacebookShares(GnuTask):
  
  """
  Since Facebook allows requests of multiple urls in one batch, we'll build up 
  all urls input and then request them in "complete"
  """

  stdout = False 

  def configure(self):
    self.urls = []

  def main(self, **kw):
    self.urls.append(kw.get('url'))

  def complete(self):
    params = {
      'method': 'links.getStats',
      'format': 'json',
      'urls': ','.join(self.urls)
    }

    try:
      r = requests.get(
        'http://api.facebook.com/restserver.php', 
        params = params
        )

    except ConnectionError as e:
      self.log.error(e)

    else:  
      # parse response
      stats = r.json()

      for row in stats:
      
        # delate normalized url
        del row['normalized_url']
      
        # add datetime 
        row['datetime'] = utc_now()
      
        write_stdout(row)

if __name__ == '__main__':
  f = FacebookShares()
  f.cli()