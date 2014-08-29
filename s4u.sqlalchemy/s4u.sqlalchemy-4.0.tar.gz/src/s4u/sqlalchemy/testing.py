import unittest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from sqlalchemy import create_engine
from pyramid_sqlalchemy.testing import DatabaseTestCase


class RoundTripTestCase(unittest.TestCase):
    @classmethod
    def setupClass(cls):
        cls.engine = create_engine('sqlite:///', echo=True)
        cls.metadata = MetaData(bind=cls.engine)
        cls.BaseObject = declarative_base(metadata=cls.metadata)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.metadata.create_all()
        self.session = self.Session()

    def tearDown(self):
        self.metadata.drop_all()

    @classmethod
    def teardownClass(cls):
        cls.Session.close_all()
        cls.engine.dispose()

__all__ = ['DatabaseTestCase']
