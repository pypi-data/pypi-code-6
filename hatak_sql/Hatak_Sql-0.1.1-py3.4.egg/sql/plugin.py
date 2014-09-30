from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from hatak.plugin import Plugin, RequestPlugin


class SqlPlugin(Plugin):

    def add_to_registry(self):
        engine = create_engine(self.settings['db:url'])
        self.config.registry['db_engine'] = engine
        self.config.registry['db'] = sessionmaker(bind=engine)()

    def add_request_plugins(self):
        self.add_request_plugin(DatabaseRequestPlugin)

    def add_unpackers(self, unpacker):
        unpacker.add('db', lambda req: req.db)
        unpacker.add('query', lambda req: req.db.query)


class DatabaseRequestPlugin(RequestPlugin):

    def __init__(self):
        super().__init__('db')

    def return_once(self):
        db = self.registry['db']
        db.flush()
        return db
