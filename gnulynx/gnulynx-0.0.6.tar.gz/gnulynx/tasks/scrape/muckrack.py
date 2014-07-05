from gnulynx import GnuTask

from journarator import journarator

class ScrapeMuckrack(GnuTask):
  
  def main(self, **kw):
    for journo in journarator():
      yield journo

if __name__ == '__main__':
  f = ScrapeMuckrack()
  f.cli()
