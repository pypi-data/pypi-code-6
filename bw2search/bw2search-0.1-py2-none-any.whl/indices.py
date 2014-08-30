from .schema import bw2_schema
from bw2data import config, Database
from whoosh import index


class IndexManager(object):
    def __init__(self, dir_name=u"whoosh"):
        self.path = config.request_dir(u"whoosh")

    def get(self):
        try:
            return index.open_dir(self.path)
        except index.EmptyIndexError:
            return self.create()

    def create(self):
        return index.create_in(self.path, bw2_schema)

    def reset(self):
        return self.create()

    def add_database(self, name):
        writer = self.get().writer()
        db = Database(name).load()

        for key, value in db.items():
            writer.add_document(
                name=value.get(u"name", u""),
                comment=value.get(u"comment", u""),
                product=value.get(u"reference product", u""),
                categories="-".join(value.get(u"categories", u"")),
                location=value.get(u"location", u""),
                database=key[0],
                key=key[1]
            )
        writer.commit()
