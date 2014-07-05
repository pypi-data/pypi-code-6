from gnulynx import GnuTask 

import dataset
import os

class SQLQuery(GnuTask):

  def configure(self, **opts):
    self.db = dataset.connect(opts.get('db_url'))
  
  def process_result(self, result):
    row = {k:v for k,v in result.items() if k != ""}
    return row

  def main(self, **kw):
    results = self.db.query(kw.get('query'))
    for result in results:
      yield self.process_result(result)

if __name__ == '__main__':
  s = SQLQuery()
  s.cli()

