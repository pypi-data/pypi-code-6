import logging
import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


_log = logging.getLogger(__name__)

Base = declarative_base()
session_factory = sessionmaker()
Session = scoped_session(session_factory)


def open_database(url):  # pragma: no cover
    engine = create_engine(url, echo=False)

    Session.configure(bind=engine)

    if os.path.exists(url[10:]):
        _log.info("Opening existing database")
        pass
    else:
        _log.info("Creating new database")
        import bdgt.models
        Base.metadata.create_all(engine)


@contextmanager
def session_scope():  # pragma: no cover
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
