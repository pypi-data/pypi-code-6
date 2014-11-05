#!/usr/bin/env 3python
"""Database: low level module for manipulating the database"""

from sqlalchemy import Table, Column, MetaData
from sqlalchemy import Integer, String, Boolean, BLOB, Binary, DateTime, Enum
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql import select
from datetime import datetime
from functools import partial
import logging

log = logging.getLogger('blitz-ca.database')

metadata = MetaData()

certs = Table('certs', metadata,
    # cn, expiry, extansions?
    Column('id', Integer, primary_key=True),
    Column('raw', BLOB, nullable=False, unique=True),
    Column('ca', Boolean, nullable=False),
    Column('common_name', String, nullable=False),
    Column('valid_before', DateTime),
    Column('valid_after', DateTime),
    Column('private_key', None, ForeignKey('keys.id')),
    Column('date', DateTime(timezone=True), nullable=False, default=datetime.utcnow),
    Column('comment', String(64)),
)

requests = Table('requests', metadata,
    Column('id', Integer, primary_key=True),
    Column('raw', BLOB, nullable=False, unique=True),
    Column('common_name', String, nullable=False),
    Column('certificate', None, ForeignKey('certs.id')),
    Column('private_key', None, ForeignKey('keys.id')),
    Column('date', DateTime(timezone=True), nullable=False, default=datetime.utcnow),
    Column('comment', String(64)),
)

# there should be no direct interaction with this table, all keys should be
# linked to requests or certs
keys = Table('keys', metadata,
    Column('id', Integer, primary_key=True),
    Column('raw', BLOB, nullable=False, unique=True),
    Column('generated_date', DateTime(timezone=True), nullable=False, default=datetime.utcnow),
    Column('key_type', Enum("RSA")),
    Column('key_strength', Integer),
    Column('comment', String(64)),
)

issued_certs = Table('issued_certs', metadata,
    Column('ca', None, ForeignKey('certs.id'), primary_key=True),
    Column('cert', None, ForeignKey('certs.id'), primary_key=True),
)

revoked_certs = Table('revoked_certs', metadata,
    Column('ca', Integer, nullable=False),
    Column('cert', Integer, nullable=False ),
    ForeignKeyConstraint(['ca', 'cert'], ['issued_certs.ca', 'issued_certs.cert']),
)


def list_cert_authorities(conn):
    """Generic function to get all data in a specific table"""
    s = select([certs, keys]).where(certs.c.ca == True)
    results = conn.execute(s)

    return results

# We want something a bit nicer to work with with the following behavior:
#database
#database.tablea
#database.table.insert
#database.table[id]
#[for i in database.table]

class Database:
    """Thin convience object to access all tables in a DB without providing a connection"""
    _tables = (certs, requests, keys, issued_certs)
    
    def __init__(self, conn):
        self._conn = conn
        self.execute = conn.execute
        
        for table in self._tables:
            setattr(self, table.name, Table(conn, table))
    
    def __str__(self):
        return "<Database: {}>".format(conn)


class Table:
    """Thin wrapper around a table object with connection baked in for some methods"""
    def __init__(self, conn, table):
        self._conn = conn
        self._table = table
        self.name = table.name
    
    def __str__(self):
        return "<table: {} {}>".format(self.name, self._conn)
    
    def __iter__(self):
        s = self._table.select()
        results = self._conn.execute(s)

        return iter(results)

    def __getitem__(self, key):
        """Generic function to get an item from a specific table"""
        s = self._table.select().where(self._table.c.id == key)
        result = self._conn.execute(s).fetchone()
        
        if result is None:
            raise KeyError("Entry not found, id:{}, table:{}".format(key, table.name))
        
        return result

    def __delitem__(self, key):
        s = self._table.delete().where(self._table.c.id == key)
        result = self._conn.execute(s)
        
        if result is None:
            raise KeyError("Entry not found, id:{}, table:{}".format(key, table.name))
        
        return result
        

    def __getattr__(self, key):
        """Proxy to table object"""
        return getattr(self._table, key)
