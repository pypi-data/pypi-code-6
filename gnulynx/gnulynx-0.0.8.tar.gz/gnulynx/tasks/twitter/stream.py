from gnulynx import GnuTask
from gnulynx.cli_util import write_stdout

from birdfeeder import Stream

class TwitterStream(GnuTask):
  
  def configure(self):
    self.stdout = False 

  def main(self, **kw):
    s = Stream(store=write_stdout)
    s.statuses.filter(**kw)

if __name__ == '__main__':
  f = TwitterStream()
  f.cli()
