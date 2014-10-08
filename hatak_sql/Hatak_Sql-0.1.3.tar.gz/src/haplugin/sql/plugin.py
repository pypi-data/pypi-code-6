from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from hatak.plugin import Plugin, RequestPlugin


class SqlPlugin(Plugin):

    def add_to_registry(self):
        engine = create_engine(self.settings['db:url'])
        self.config.registry['db_engine'] = engine
        self.config.registry['db'] = sessionmaker(bind=engine)()

    def add_request_plugins(self):
        if self.settings['db:url'].startswith('sqlite'):
            self.add_request_plugin(SqliteRequestPlugin)
        else:
            self.add_request_plugin(DatabaseRequestPlugin)

    def add_unpackers(self):
        self.unpacker.add('db', lambda req: req.db)
        self.unpacker.add('query', lambda req: req.db.query)


class DatabaseRequestPlugin(RequestPlugin):

    def __init__(self):
        super().__init__('db')

    def return_once(self):
        db = self.registry['db']
        db.flush()
        return db


class SqliteRequestPlugin(DatabaseRequestPlugin):

    def return_once(self):
        engine = self.registry['db_engine']
        self.registry['db'] = sessionmaker(bind=engine)()
        return super().return_once()
