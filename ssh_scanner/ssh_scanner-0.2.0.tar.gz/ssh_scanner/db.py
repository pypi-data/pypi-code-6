#!/usr/bin/env python
import sys

from sqlalchemy import (
    create_engine, 
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime,
)

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Host(Base):
    __tablename__ = 'host'
    host_id = Column(Integer, primary_key=True)
    hostname = Column(String)
    ip = Column(String(64))
    port = Column(Integer)
    state = Column(String(64))
    version = Column(String)
    banner = Column(String)
    keys = relationship('Key', backref='host')

    def __repr__(self):
        return 'Host(%s, %s, port=%s, state=%s, keys=[%s])' % (
            self.hostname,
            self.ip,
            self.port,
            self.state,
            ','.join([str(k) for k in self.keys]),
        )

    def __str__(self):
        return self.__repr__()

class Key(Base):
    __tablename__ = 'key'
    key_id = Column(Integer, primary_key=True)
    host_id = Column(Integer, ForeignKey('host.host_id'))
    typ = Column(String)
    size = Column(Integer)
    fingerprint = Column(String)

    def __repr__(self):
        return '%s(%s)' % (self.typ, self.size)

    def __str__(self):
        return self.__repr__()

def create_session(engine_path):
    from sqlalchemy.engine.reflection import Inspector
    try:
        eng = create_engine(engine_path)
        inspector = Inspector.from_engine(eng)
    except OperationalError:
        sys.stderr.write('Invalid postgres creds\n'
            'Please create database sshscanner and grant privs to user\n')
        sys.exit(1)
    tables = list(inspector.get_table_names())
    if 'key' not in tables or 'host' not in tables:
        Base.metadata.create_all(eng)
    Session = sessionmaker(bind=eng)
    return Session()

def connect(username, password):
    eng_path = 'postgresql://%(username)s:%(password)s@localhost:5432/sshscanner' % {'username': username, 'password': password}
    return create_session(eng_path)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('username')
    parser.add_argument('password')
    args = parser.parse_args()
    sesh = connect(args.username, args.password)
    print('%-20s %-15s' % ('Hostname', 'IP'))
    for host in sesh.query(Host).all():
        print('%-20s %-15s' % (host.hostname, host.ip))

