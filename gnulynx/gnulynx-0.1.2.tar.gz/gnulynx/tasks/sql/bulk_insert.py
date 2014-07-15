#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnulynx import GnuTask 

import dataset

from util import get_types

class SQLInsertMany(GnuTask):
  
  stdout = False

  def configure(self):

    # connect to db, etc.
    self.db = dataset.connect(self.opts.get('db_url'))
    self.table = self.opts.get('table')
    self.types = get_types(self.opts.get('schema'))
    self.data = []
    
  def main(self, **kw):

    # store input in a list 
    self.data.append(kw)

  def complete(self):

    # on completion of task, insert all records
    self.db[self.table].insert_many(self.data, types=self.types)

if __name__ == '__main__':
  s = SQLInsertMany()
  s.cli()
