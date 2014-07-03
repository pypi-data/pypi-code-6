from gnulynx import GnuTask

from pageone import PageOne

class HomepageLinkStats(GnuTask):
  
  def main(self, **kw):
    p = PageOne(**kw)

    # only pass relevant 
    # kwargs to function
    subkw = {
      'incl_external': kw.get('incl_external', None),
      'pattern': kw.get('pattern')
    }
    return p.link_stats(**subkw)
    
if __name__ == '__main__':
  f = HomepageLinkStats()
  f.run()
