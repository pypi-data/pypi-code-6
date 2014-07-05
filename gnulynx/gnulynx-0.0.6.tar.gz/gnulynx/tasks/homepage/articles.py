from gnulynx import GnuTask

from pageone import PageOne

class HomepageArticles(GnuTask):
    
  def main(self, **kw):
    p = PageOne(**kw)

    # only pass relevant 
    # kwargs to function
    urls = p.articles(**self.opts)

    for u in urls:
      yield {'url': u}

if __name__ == '__main__':
  f = HomepageArticles()
  f.cli()
