"""Mirador Result class

.. moduleauthor Nick Jacob <nick@mirador.im>

"""
from errors import http_exceptions, MiradorException
import sys
import json


class MiradorResultList(object):

    def __init__(self, items=[]):
        self._items = {}

    def _add(self, items=[]):
        for x in items:
            self._items[x.id] = x

    def concat(self, more=[]):
        self._add(more)

    def __getitem__(self, n):

        if n in self._items:
            return self._items[n]

        return None

    def __iter__(self):
        sys.stderr.write("""
[DeprecationWarning]
Classification methods not return a dict indexed by id
""")
        for k, v in self._items.items():
            yield k, v

    def __len__(self):
        return len(self._items)

    def items(self):
        return self._items.items()


class MiradorResult(object):
    """A result from the Mirador API.
    Contains fields indicating classification result:
        safe - boolean indicating flagging status
        value - a float 0.0-1.0; confidence of result
    """

    FMT_STR = "<MiradorResult: {id}; safe: {safe}; value: {value}/>"

    def __init__(self, raw={}):

        if 'result' not in raw:
            raise http_exceptions[500]("bad result: {}".format(raw))

        res = raw['result']

        if 'safe' not in res or 'value' not in res:

            if 'errors' in res:
                self.errors = res['errors']

            raise http_exceptions[500]("bad result: {}".format(raw))

        self.id = raw.get('id', raw.get('url', None))
        self.safe = res['safe']
        self.value = res['value']

    @property
    def name(self):
        sys.stderr.write("""
[DeprecationWarning]:
MiradorResult.name has been depricated in favor of @id
""")
        return self.id

    @name.setter
    def name(self, value=None):
        sys.stderr.write("""
[DeprecationWarning]:
MiradorResult.name has been depricated in favor of @id
""")
        self.id = value

    @staticmethod
    def parse_results(results):
        """ parse JSON output of API into MiradorResult objects """

        if not results:
            raise http_exceptions[500](
                "no result available: {}"
                .format(results)
            )

        return [MiradorResult(r) for r in results]

    @staticmethod
    def parse_results_safe(reqs, results):
        "parse results and catch errors in bad results"
        if not results:
            return None

        try:
            return [
                MiradorResult(n, r)
                for n, r in zip(reqs, results)
            ]
        except MiradorException:
            return None

    def __repr__(self):
        return self.FMT_STR.format(**self.__dict__)

    def __str__(self):
        return self.FMT_STR.format(**self.__dict__)

    def to_json(self):
        return json.dumps({
            'id': self.id,
            'value': self.value,
            'safe': self.safe
        })
