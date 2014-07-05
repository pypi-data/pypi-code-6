from gnulynx import GnuTask

import birdfeeder 

class TwitterList(GnuTask):

  def main(self, **kw):
    return birdfeeder.list_timeline(
      **dict(kw.items() + self.opts.items())
      )

if __name__ == '__main__':
  f = TwitterList()
  f.cli()
