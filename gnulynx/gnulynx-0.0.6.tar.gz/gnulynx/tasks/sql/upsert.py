from gnulynx import GnuTask 

import dataset

class SQLUpsert(GnuTask):

  def configure(self, **opts):
    self.db = dataset.connect(opts.get('db_url'))
    self.table = opts.get('table')
    self.primary_keys = opts.get('primary_keys')
    self.stdout = False
    
  def main(self, **kw):
    # insert
    self.db[self.table].upsert(kw, self.primary_keys)

if __name__ == '__main__':
  s = SQLUpsert()
  s.cli()
