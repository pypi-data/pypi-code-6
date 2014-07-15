#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnulynx import GnuTask 

import dataset

from util import get_types

class SQLInsert(GnuTask):
  
  stdout = False
  
  def configure(self):
    self.db = dataset.connect(self.opts.get('db_url'))
    self.table = self.opts.get('table')
    self.types = get_types(self.opts.get('schema'))

    
  def main(self, **kw):
    # insert
    self.db[self.table].insert(kw, types=self.types)

if __name__ == '__main__':
  s = SQLInsert()
  s.cli()
