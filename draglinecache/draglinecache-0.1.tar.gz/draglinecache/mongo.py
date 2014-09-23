from .cache import Cache
from datetime import datetime
from pymongo import MongoClient
try:
    import cPickle as pickle
except ImportError:
    import pickle


class MongoCache(Cache):
    def initilize(self, host='localhost', database='dragline', collection='cache'):
        self.collection = MongoClient(host)[database][collection]

    def set(self, key, value):
        dump = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        data = dict(_id=key, content=dump.decode(value.encoding), time=datetime.now(),
                    encoding=value.encoding)
        self.collection.save(data)

    def get(self, key):
        d = datetime.now() - self.validity
        data = dict(_id=key, time={'$gt': datetime.now() - self.validity})
        doc = self.collection.find_one(data)
        if doc is None:
            return doc
        return pickle.loads(doc['content'].encode(doc['encoding']))
