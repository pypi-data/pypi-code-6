from gnulynx import GnuTask

import zuckup

class FacebookPageStats(GnuTask):
  
  def main(self, **kw):
    yield zuckup.page_stats(**kw)

if __name__ == '__main__':
  f = FacebookPageStats()
  f.cli()
