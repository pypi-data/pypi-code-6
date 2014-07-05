from gnulynx import GnuTask

from superss import SupeRSS

class RSSFeed(GnuTask):

  def main(self, **kw):
    s = SupeRSS(
      kw.get('feed'), 
      **self.opts
      )
    return s.run()

if __name__ == '__main__':
  f = RSSFeed()
  f.cli()
