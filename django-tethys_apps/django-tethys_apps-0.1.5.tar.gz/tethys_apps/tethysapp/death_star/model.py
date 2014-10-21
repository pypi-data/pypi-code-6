from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

from .utilities import get_persistent_store_engine

# DB Engine, sessionmaker, and base
engine = get_persistent_store_engine('example_db')
SessionMaker = sessionmaker(bind=engine)
Base = declarative_base()


class CrewMember(Base):
    """
    Example SQLAlchemy model
    """
    __tablename__ = 'crew_members'

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)