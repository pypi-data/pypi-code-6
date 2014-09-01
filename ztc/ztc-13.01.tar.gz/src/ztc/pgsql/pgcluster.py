#!/usr/bin/env python
"""
PgCluster ZTCCheck
Used to perform database-wide checks (like querying each database of the cluster)

Copyright (c) pg_check.pl authors
Copyright (c) 2010-2011 Vladimir Rusinov <vladimir@greenmice.info>
Copyright (c) 2011 Wrike, Inc. [http://www.wrike.com]
"""

import heapq

from ztc.check import ZTCCheck, CheckFail
from ztc.pgsql.pgconn import PgConn
import ztc.pgsql.queries as pgq

class PgCluster(ZTCCheck):
    """ Class represent database cluster """
    
    name = 'pgsql'
    
    OPTPARSE_MIN_NUMBER_OF_ARGS = 1
    
    dbs = []
    
    def _get(self, metric, *args, **kwargs):
        if metric == 'bloat':
            return self.get_bloat()
        else:
            raise CheckFail('uncknown metric')
        
    def get_bloat(self):
        """ get max database bloat of all databases of cluster """
        q = pgq.BLOAT
        pages = 0
        otta = 0
        bloatest = [] # list of bloatest tables
        ret = self.query_eachdb(q, exclude=['template0'])
        for db in ret.keys():
            # loop through all databases
            for r in ret[db]:
                # and its tables
                pages += r[4]
                otta += r[5]
                if pages > 1000:
                    # add to list of bloatest tables
                    bloat = 100 - 100*(pages-otta) / pages
                    item = (bloat, "%s.%s.%s->%s" % (db, r[0], r[1], r[2]))
                    if len(bloatest) < 5:
                        heapq.heappush(bloatest, item)
                    else:
                        heapq.heapreplace(bloatest, item)
        self.logger.debug("pages: %i, otta: %i" % (pages, otta))
        while len(bloatest):
            b = heapq.heappop(bloatest)
            self.logger.debug("bloatest: %s: %.2f%%" % (b[1], 100-b[0]))
        if pages < 5000: # cluster < then 40 Mb is no serious
            return 0
        else:
            return 100*(pages - otta) / pages
    
    # lower-level functions
    def get_dblist(self):
        connect_dict = {
            'host': self.config.get('host', None), # none = connect via socket
            'user': self.config.get('user', 'postgres'),
            'password': self.config.get('password', None),
            'database': self.config.get('database', 'postgres')
        }        
        d = PgConn(connect_dict, self.logger)
        dbs = d.query("SELECT datname FROM pg_database")
        self.dbs = [x[0] for x in dbs]
    
    def query_eachdb(self, sql, exclude=[]):
        """ execure query on each database of the cluster
        Params:
            sql (string): query text
            exclude (list of strings): database names to exclude
        Out:
            { dbname: query_result, ...  }
        """
        
        connect_dict = {
            'host': self.config.get('host', None), # none = connect via socket
            'user': self.config.get('user', 'postgres'),
            'password': self.config.get('password', None),
            'database': self.config.get('database', 'postgres')
        }        
        
        ret = {}
        if not self.dbs: self.get_dblist()
        for db in self.dbs:
            if db in exclude:
                continue
            connect_dict['database'] = db
            pdb = PgConn(connect_dict, self.logger)
            ret[db] = pdb.query(sql)
        return ret
