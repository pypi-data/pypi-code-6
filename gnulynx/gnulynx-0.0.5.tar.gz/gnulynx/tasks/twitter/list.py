from gnulynx import GnuTask

import birdfeeder 

class TwitterList(GnuTask):

  def main(self, **kw):
    return birdfeeder.list_timeline(**kw)

if __name__ == '__main__':
  f = TwitterList()
  f.run()
