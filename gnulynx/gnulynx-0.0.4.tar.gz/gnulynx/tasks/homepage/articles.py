from gnulynx import GnuTask

from pageone import PageOne

class HomepageArticles(GnuTask):
  
  def main(self, **kw):
    p = PageOne(**kw)
    
    # only pass relevant 
    # kwargs to function
    subkw = {
      'incl_external': kw.get('incl_external', None),
      'pattern': kw.get('pattern')
    }
    for a in p.articles(**subkw):
      yield {'url': a}

if __name__ == '__main__':
  f = HomepageArticles()
  f.run()
