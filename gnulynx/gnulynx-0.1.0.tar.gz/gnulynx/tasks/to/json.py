#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys 

from gnulynx import GnuTask
from gnulynx.serialize import to_json

class ToJson(GnuTask):
  
  stdout = False 

  def configure(self):
    self.data = []

  def main(self, **kw):
    self.data.append(kw)

  def complete(self):
    s = to_json(self.data)
    print(s, file=sys.stdout)

if __name__ == '__main__':
  s = ToJson()
  s.cli()
