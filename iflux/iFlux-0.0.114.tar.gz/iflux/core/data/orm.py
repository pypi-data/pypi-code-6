__author__ = 'fpiraz'
import functools
import sys

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Session = sessionmaker()

class SqlalchemyEnabled():

    @property
    def sqlalchemy_engine(self):
        """
        Returns a Sqlalchemy engine instance
        """
        return getattr(self, '__slqalchemy_engine')

    @property
    def sqlalchemy_session(self):
        """
        Returns a Sqlalchemy Session instance
        """
        return getattr(self, '__slqalchemy_session')

