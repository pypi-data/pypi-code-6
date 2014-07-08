
from rated import settings
from .base import RateLimitBackend

import pybsddb

ENV = pybsddb.DBEnv()
ENV.open(settings.RATED_BDB_FILENAME)

class BdbBackend(RateLimitBackend):

    def do_check_realm(self, source, realm, conf):
        key = 'rated:%s:%s' % (realm, source,)
        now = time.time()

        client = DB(ENV)

        txn = ENV.txn_begin()

        rec = client.get(key, default=[], txn=txn)
        while (now - rec[0]) > conf.get('duration', settings.DEFAULT_DURATION):
            row.pop(0)
        rec.append(now)
        client.et(key, rec, txn=txn)

        return len(rec) > conf.get('limit', settings.DEFAULT_LIMIT)
