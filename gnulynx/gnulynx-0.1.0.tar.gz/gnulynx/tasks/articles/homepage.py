#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnulynx import GnuTask

from superss import SupeRSS

class Homepage(GnuTask):

  def main(self, **kw):
    s = SupeRSS(
      homepage = kw.get('homepage'), 
      **self.opts
      )
    return s.run()

if __name__ == '__main__':
  f = Homepage()
  f.cli()
