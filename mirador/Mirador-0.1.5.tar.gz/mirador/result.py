"""Mirador Result class

.. moduleauthor Nick Jacob <nick@mirador.im>

"""
from errors import http_exceptions, MiradorException


class MiradorResult(object):
    """A result from the Mirador API.
    Contains fields indicating classification result:
        safe - boolean indicating flagging status
        value - a float 0.0-1.0; confidence of result
    """

    FMT_STR = "<MiradorResult: {name}; safe: {safe}; value: {value}/>"

    def __init__(self, name, raw={}):

        if 'result' not in raw:
            raise http_exceptions[500]("bad result: {}".format(raw))

        res = raw['result']

        if 'safe' not in res or 'value' not in res:

            if 'errors' in res:
                self.errors = res['errors']

            raise http_exceptions[500]("bad result: {}".format(raw))

        self.name = name
        self.safe = res['safe']
        self.value = res['value']

    @staticmethod
    def parse_results(reqs, results):
        """ parse JSON output of API into MiradorResult objects """

        if not results:
            raise http_exceptions[500]("no result available: {}".format(reqs))

        return [
            MiradorResult(n, r)
            for n, r in zip(reqs, results)
        ]

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
