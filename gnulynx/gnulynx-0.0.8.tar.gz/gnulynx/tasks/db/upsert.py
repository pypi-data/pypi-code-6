#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnulynx import GnuTask 

import dataset

class DBUpsert(GnuTask):
  
  stdout = False

  def configure(self):
    self.db = dataset.connect(self.opts.get('db_url'))
    self.table = self.opts.get('table')
    self.primary_keys = self.opts.get('primary_keys')
    
  def main(self, **kw):
    # insert
    self.db[self.table].upsert(kw, self.primary_keys)

if __name__ == '__main__':
  s = DBUpsert()
  s.cli()
