import g11pyutils as utils
import pymongo
import logging
from datetime import datetime

LOG = logging.getLogger("MongoDB")


class MongoDB(object):
    def __init__(self, spec, host='127.0.0.1', port=27017, buff=1000, id_field=None, updated_field='_updated', upsert=False):
        """
        Constructs a MongoDB output
        :param spec: A string for embedding options, e.g. 'host=example.com,port=80,id=_id,ts=created:updated
        :param host: The MongoDB host, defaults to localhost
        :param port: The MongoDB port, defaults to 27017, the default MongoDB port
        :param buff: The number of documents to accumulate for each DB TX
        :param id_field: The event field that should be used as the ID
        :param ts_fields: The event field(s), colon delimited, that should be parsed as ISO8601 timestamps
        """
        LOG.warn(pymongo.get_version_string())
        args = spec.split(",", 1)
        self.db_name, self.coll = args[0].split(".")
        opts = utils.to_dict(args[1]) if len(args) > 1 else {}
        self.host = opts.get("host", host)
        self.port = opts.get("port", port)
        self.buffer = opts.get("b", buff)
        self.id_field = opts.get("id", id_field)
        self.updated_field = opts.get("updated", updated_field)
        self.upsert = ('%s' % opts.get("upsert", upsert)).lower() == "true"

        def do_connect():
            return self.do_connect()

        def do_close():
            return self.do_close(self.conn)

        self.conn = utils.Connector(do_connect, do_close)
        self.conn.connect()

    def do_connect(self):
        mongo_client = pymongo.MongoClient(self.host, self.port)
        self.collection(mongo_client) # verify
        return mongo_client

    def db(self, cli=None):
        mongo_client = cli if cli else self.conn.c()
        if not mongo_client:
            raise Exception("Not connected")
        if not self.db_name in mongo_client.database_names():
            raise ValueError("No database named '%s'", self.db_name)
        return mongo_client[self.db_name]

    def collection(self, cli=None):
        db = self.db(cli)
        if not self.coll in db.collection_names():
            raise ValueError("Database '%s' has no collection named '%s'" % (self.db, self.coll))
        return db[self.coll]

    def do_close(self, conn):
        conn.close()

    def send(self, docs):
        c = self.collection()
        while True:
            try:
                #bulk = c.initialize_unordered_bulk_op()
                #bulk.insert(docs)
                #bulk.execute()
                #if self.id_field:
                #    c.update({"_id" : })
                if self.upsert:
                    inserts = []
                    upserts = []
                    for d in docs:
                        if '_id' in d:
                            upserts.append(d)
                        else:
                            inserts.append(d)
                    if inserts:
                        LOG.info("Inserting %s new docs" % len(docs))
                        c.insert(inserts)
                    if upserts:
                        LOG.info("Upserting %s docs" % len(docs))
                        bulk = c.initialize_ordered_bulk_op()
                        for u in upserts:
                            bulk.find({'_id': u.pop('_id')}).upsert().update({'$set': u})
                        bulk.execute()
                else:
                    LOG.info("Inserting %s docs" % len(docs))
                    c.insert(docs, manipulate=False, continue_on_error=True)
                break
            except pymongo.errors.DuplicateKeyError as dke:
                LOG.warn(dke)
                break
            except Exception as ex:
                LOG.warn("Bulk insert failed: %s", ex)
                if self.is_connect_err(ex):
                    self.conn.reconnect()
                else:
                    break

    def is_connect_err(self, ex):
        if repr(ex).find('E11000') >= 0:
            return False
        return True

    def process(self, pin):
        buff = []
        for e in pin:
            if self.id_field: # Set ID if an ID field was specified
                e['_id'] = e.pop(self.id_field)
            if self.updated_field and self.updated_field in e:
                try:
                    uf = e[self.updated_field]
                    e['_updated'] = uf if isinstance(uf, datetime) else parse_iso8601(uf)
                    if self.updated_field != '_updated':
                        e.pop(self.updated_field)  # Only if 1st step completes
                except Exception, ex:
                    LOG.warn("Exception parsing updated date: %s, %s" % (ex, ex.message))
            LOG.debug("Inserting %s", e)
            buff.append(e)
            if len(buff) >= self.buffer:
                self.send(buff)
                buff = []
        if buff:
            self.send(buff)


def parse_iso8601(s):
    """Parses a standard ISO8601 date into a python datetime for insertion into MongoDB"""
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')