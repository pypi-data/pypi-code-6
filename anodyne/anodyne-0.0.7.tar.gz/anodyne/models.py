import sys

from sqlalchemy.ext import declarative
from anodyne import engines

ModelBase = declarative.declarative_base()


def setup(database):
    engine_data = engines.get_engine(database)
    ModelBase.metadata.create_all(engine_data.get("engine"))


def load_models(database, models_module):
    if models_module is not None:
        if models_module not in sys.modules.keys():
            __import__(models_module)
    engine_data = engines.get_engine(database)
    ModelBase.metadata.create_all(engine_data.get("engine"))
