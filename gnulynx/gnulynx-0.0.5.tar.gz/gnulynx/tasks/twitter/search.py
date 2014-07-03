from gnulynx import GnuTask

import birdfeeder

class TwitterSearch(GnuTask):

  def main(self, **kw):
    return birdfeeder.search(**kw)

if __name__ == '__main__':
  f = TwitterSearch()
  f.run()
