from gnulynx import GnuTask

import zuckup 

class FacebookPage(GnuTask):
  
  def main(self, **kw):
    return zuckup.page(**kw)

if __name__ == '__main__':
  f = FacebookPage()
  f.cli()
