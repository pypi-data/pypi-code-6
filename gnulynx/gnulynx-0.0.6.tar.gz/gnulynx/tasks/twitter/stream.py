from gnulynx import GnuTask
from gnulynx.util import write_stdout

from birdfeeder import Stream

class TwitterStream(GnuTask):
  
  def configure(self, **opts):
    self.stdout = False 

  def main(self, **kw):
    s = Stream(store=write_stdout)
    s.statuses.filter(**kw)

if __name__ == '__main__':
  f = TwitterStream()
  f.cli()
