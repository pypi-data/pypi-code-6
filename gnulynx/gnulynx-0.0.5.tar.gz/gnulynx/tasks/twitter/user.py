from gnulynx import GnuTask

import birdfeeder

class TwitterUser(GnuTask):

  def main(self, **kw):
    return birdfeeder.user_timeline(**kw)

if __name__ == '__main__':
  f = TwitterUser()
  f.run()
