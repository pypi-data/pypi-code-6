#!/usr/bin/env python
"""
PgDB class - ZTCCheck for tracking single postgresql database
    
Copyright (c) 2010-2011 Vladimir Rusinov <vladimir@greenmice.info>

Requirements:
    * PostgreSQL 8.3 or older
    * pg_buffercache from contrib installed on configured db/user
"""

import time

from ztc.check import ZTCCheck, CheckFail
import ztc.pgsql.queries as pgq
from ztc.pgsql.pgconn import PgConn

class PgDB(ZTCCheck):
    """ Connection to single database """
    
    name= 'pgsql'
    dbconn = None
    
    OPTPARSE_MIN_NUMBER_OF_ARGS = 1
    OPTPARSE_MAX_NUMBER_OF_ARGS = 3
    
    def _myinit(self):
        connect_dict = {
            'host': self.config.get('host', None), # none = connect via socket
            'user': self.config.get('user', 'postgres'),
            'password': self.config.get('password', None),
            'database': self.config.get('database', 'postgres')
        }
        self.dbconn = PgConn(connect_dict, self.logger)        
    
    def _get(self, metric, *args, **kwargs):
        if metric == 'query':
            q = args[0]
            return self.dbconn.query(q)
        elif metric == 'autovac_freeze':
            return self.get_autovac_freeze()
        elif metric == 'ping':
            return self.get_ping()
        elif metric == 'tnxage':
            state = args[0]
            return self.get_tnx_age(state)
        elif metric == 'buffers':
            buf_metric = args[0]
            return self.get_buffers(buf_metric)
        elif metric == 'conn':
            state = args[0]
            return self.get_conn_nr(state)
        elif metric == 'dbstat':
            m = args[0]
            return self.get_dbstat(m)
        elif metric == 'fsm':
            m = args[0]
            return self.get_fsm(m)
        elif metric == 'locks':
            m = args[0]
            mm = args[1]
            return self.get_locks(m, mm)
        elif metric == 'wal':
            m = args[0]
            if m == 'num':
                return self.get_wal_num()
            else:
                CheckFail('uncknown wal metric: %s' % m)                            
        else:
            raise CheckFail('uncknown metric %s' % metric)
        
    def get_fsm(self, metric):
        """ PostgreSQL freespacemap metrics.
        Requirements: pg_freespacement, PostgreSQL <= 8.3"""
        q = pgq.FSM[metric]
        ret = self.dbconn.query(q)[0][0]
        return ret
    
    def get_buffers(self, metric):
        """ PostgreSQL buffer metrics: number of clear/dirty/used/total
        buffers.
        Requirements: pg_buffercache contrib """
        q = pgq.BUFFER[metric]
        ret = self.dbconn.query(q)[0][0]
        return ret
        
    def get_dbstat(self, m):
        """ get sum of passed metric from dbstat """
        q = "SELECT SUM(%s) FROM pg_stat_database" % m
        ret = self.dbconn.query(q)[0][0]
        return ret
        
    def get_conn_nr(self, state):
        """ Get number of connections in given state """
        q = pgq.CONN_NUMBER[state]
        ret = self.dbconn.query(q)[0][0]
        return ret
        
    def get_tnx_age(self, state):
        """ Get max age of transactions in given state.
        Supported states are: 'running', 'idle_tnx'
        """
        if state == 'idle_tnx':
            q = pgq.TNX_AGE_IDLE_TNX
        elif state == 'running':
            q = pgq.TNX_AGE_RUNNING
        else:
            raise CheckFail("uncknown transaction state requested")
        
        ret = self.dbconn.query(q)
        if ret:
            ret = ret[0][0]
            return abs(ret)
        else:
            # no rows returned => no transactions in given state
            return 0
    
    def get_ping(self):
        st = time.time()
        try:
            if self.dbconn.query('SELECT 1'):
                return time.time() - st
            else:
                return 0
        except:
            return 0        
    
    def get_autovac_freeze(self):
        """ Checks how close each database is to the Postgres
            autovacuum_freeze_max_age setting. This action will only work for
            databases version 8.2 or higher. The 'age' of the transactions in
            each database is compared to the autovacuum_freeze_max_age setting
            (200 million by default) to generate a rounded percentage.
        
        Returns: (float) maximum age of transaction from all databases, in %
            (compared to autovacuum_freeze_max_age)
        """
        max_percent = 0
        q = pgq.AUTOVAC_FREEZE
        ret = self.dbconn.query(q)
        for (freeze, age, percent, dbname) in ret:
            if self.debug:
                self.logger.info("Freeze %% for %s: %s" % (dbname, percent))
            max_percent = max(max_percent, percent)        
        return max_percent

    def get_locks(self, m, mm=None):
        """ get number of database locks """
        if m == 'mode':
            q = pgq.LOCKS_BY_MODE[mm.lower()]
        else:
            q = pgq.LOCKS[m]
        ret = self.dbconn.query(q)[0][0]
        return ret
    
    def get_wal_num(self):
        """ get number of wal files in pg_xlog directory """
        q = pgq.WAL_NUMBER
        ret = self.dbconn.query(q)[0][0]
        return ret
