#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys 

from gnulynx import GnuTask
from gnulynx.serialize import to_json, to_gz

class ToJsonGZ(GnuTask):
  
  stdout = False 

  def configure(self):
    self.data = []

  def main(self, **kw):
    self.data.append(kw)

  def complete(self):
    s = to_json(self.data)
    print(to_gz(s), file=sys.stdout)

if __name__ == '__main__':
  s = ToJsonGZ()
  s.cli()
