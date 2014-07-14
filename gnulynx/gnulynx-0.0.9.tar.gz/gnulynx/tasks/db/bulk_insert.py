#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnulynx import GnuTask 

import dataset

class DBInsertMany(GnuTask):
  
  stdout = False

  def configure(self):

    # connect to db, etc.
    self.db = dataset.connect(self.opts.get('db_url'))
    self.table = self.opts.get('table')
    self.data = []
    
  def main(self, **kw):

    # store input in a list 
    self.data.append(kw)

  def complete(self):

    # on completion of task, insert all records
    self.db[self.table].insert_many(self.data)

if __name__ == '__main__':
  s = DBInsertMany()
  s.cli()
