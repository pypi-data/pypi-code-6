from gnulynx import GnuTask

import zuckup

class FacebookInsights(GnuTask):

  def main(self, **kw):
    return zuckup.insights(
      **dict(kw.items + self.opts.items())
    )

if __name__ == '__main__':
  f = FacebookInsights()
  f.cli()
