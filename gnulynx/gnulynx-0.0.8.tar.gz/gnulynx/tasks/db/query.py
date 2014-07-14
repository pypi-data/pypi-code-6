#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gnulynx import GnuTask 

import dataset
import os

class DBQuery(GnuTask):

  def configure(self):
    self.db = dataset.connect(self.opts.get('db_url'))
  
  def process_result(self, result):
    """
    TODO: FIX THIS HACK!
    """
    row = {}
    for k,v in result.items():
      if k != "":
        row[k] = v
    return row

  def main(self, **kw):
    results = self.db.query(kw.get('query'))
    for result in results:
      yield self.process_result(result)

if __name__ == '__main__':
  s = DBQuery()
  s.cli()

