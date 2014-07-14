#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnulynx import GnuTask 

import dataset

class DBInsert(GnuTask):
  
  stdout = False
  
  def configure(self):
    self.db = dataset.connect(self.opts.get('db_url'))
    self.table = self.opts.get('table')
    
  def main(self, **kw):
    # insert
    self.db[self.table].insert(kw)

if __name__ == '__main__':
  s = DBInsert()
  s.cli()
