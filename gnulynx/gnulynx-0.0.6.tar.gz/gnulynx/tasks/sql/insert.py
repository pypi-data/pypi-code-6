from gnulynx import GnuTask 

import dataset

class SQLInsert(GnuTask):

  def configure(self, **opts):
    self.db = dataset.connect(opts.get('db_url'))
    self.table = opts.get('table')
    self.stdout = False
    
  def main(self, **kw):
    # insert
    self.db[self.table].insert(kw)

if __name__ == '__main__':
  s = SQLInsert()
  s.cli()
