from gnulynx import GnuTask

import birdfeeder

class TwitterSearch(GnuTask):

  def main(self, **kw):
    return birdfeeder.search(
      **dict(kw.items() + self.opts.items())
      )

if __name__ == '__main__':
  f = TwitterSearch()
  f.cli()
