from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from hatak.plugin import Plugin


class SqlPlugin(Plugin):

    def add_to_registry(self):
        engine = create_engine(self.settings['db:url'])
        self.config.registry['db_engine'] = engine
        self.config.registry['db'] = sessionmaker(bind=engine)()
        self.config.add_request_method(self.add_db, 'db', reify=True)

    def add_db(self, request):
        db = request.registry['db']
        db.flush()
        return db

    def add_unpackers(self, unpacker):
        unpacker.add('db', lambda req: req.db)
        unpacker.add('query', lambda req: req.db.query)
