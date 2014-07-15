from gnulynx import GnuTask

import birdfeeder 

class TwitterUserStats(GnuTask):
  
  def main(self, **kw):
    yield birdfeeder.user_stats(**kw)

if __name__ == '__main__':
  f = TwitterUserStats()
  f.cli()
