from gnulynx import GnuTask

import zuckup

class FacebookInsights(GnuTask):

  def main(self, **kw):
    return zuckup.insights(**kw)

if __name__ == '__main__':
  f = FacebookInsights()
  f.cli()
