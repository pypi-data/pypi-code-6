from gnulynx import GnuTask

from pageone import PageOne

class HomepageLinkStats(GnuTask):
  
  def main(self, **kw):
    p = PageOne(**kw)

    # only pass relevant 
    # kwargs to function
    return p.link_stats(**self.opts)

if __name__ == '__main__':
  f = HomepageLinkStats()
  f.cli()
