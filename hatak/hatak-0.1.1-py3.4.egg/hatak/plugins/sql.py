from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .plugin import Plugin


class SqlPlugin(Plugin):

    def add_to_registry(self):
        engine = create_engine(self.settings['db:url'])
        self.config.registry['db'] = sessionmaker(bind=engine)()
        self.config.registry['db_engine'] = engine

    def add_unpackers(self, unpacker):
        unpacker.add('db', lambda req: req.registry['db'])
        unpacker.add('query', lambda req: req.registry['db'].query)
