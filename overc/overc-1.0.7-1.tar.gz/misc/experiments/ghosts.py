#! /usr/bin/env python

"""
Okay, let's assume we have a table, and someone is adding entries into it.

We have N processes, which can't talk to each other: they only see the table. Ghosts =\
Each ghost has a task: check entries as soon as they arrive, and mark them as "checked".

Problem: synchronize them so they do not clash
"""

DB_CONNECTION = 'mysql://overc:overc@127.0.0.1/overc'
GHOSTS_N = 3

#region Models

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, Boolean, DateTime

from datetime import datetime

Base = declarative_base()

class Entry(Base):
    __tablename__ = '__entries'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    checked = Column(DateTime, nullable=True)

    __mapper_args__ = {
        'version_id_col': checked,
        'version_id_generator': False
    }

#endregion

#region DB

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

def init_engine():
    """ Init engine (each thread needs to have its own engine & Session!
    :rtype: sqlalchemy.engine.base.Engine
    """
    return create_engine(DB_CONNECTION, convert_unicode=True)

def init_Session(engine):
    """ Init session class """
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

#endregion

#region Threads

from time import sleep
from random import uniform
from multiprocessing import Process
from sqlalchemy.orm.exc import StaleDataError

def _check_entries(ssn, pid):
    """ Check entries. And yes, this takes some time! """
    last_checked_id = None

    entries = ssn.query(Entry).filter(Entry.checked==None).order_by(Entry.id.asc()).all()
    for e in entries:
        last_checked_id = e.id
        e.checked = datetime.utcnow()  # Will become a valid version
        ssn.add(e)
    sleep(0.5)  # Yes, this takes some time!
    ssn.commit()

    print '{}: Checked {}'.format(pid, last_checked_id)
    return last_checked_id

def ghost(pid):
    """ Ghost process: check entries """
    sleep(1)  # Give the main thread some time to create tables

    engine = init_engine()
    Session = init_Session(engine)

    while True:
        sleep(3)

        # Supervise
        try:
            ssn = Session()
            try:
                _check_entries(ssn, pid)
            except StaleDataError as e:
                print '{}: another thread is messing up'.format(pid)
                sleep(5)  # Seems like another thread is working
        finally:
            Session.remove()

for n in range(0, GHOSTS_N):
    p = Process(target=ghost, name='Ghost {}'.format(n), args=(n,))
    p.daemon = True
    p.start()

#endregion

#region Entries source

engine = init_engine()
Session = init_Session(engine)
# Base.query = Session.query_property()
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

try:
    ssn = Session()
    while True:
        entry = Entry(checked=None)
        ssn.add(entry)
        ssn.commit()

        #print 'Added {}'.format(entry.id)
        sleep(1)
finally:
    Session.remove()

#endregion
