from gnulynx import GnuTask

import zuckup 

class FacebookPage(GnuTask):
  
  def main(self, **kw):
    return zuckup.page(
      **dict(kw.items + self.opts.items())
    )

if __name__ == '__main__':
  f = FacebookPage()
  f.cli()
