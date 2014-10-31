from collections import namedtuple


ParsedTx = namedtuple('ParsedTx', ['date', 'amount', 'account', 'description'])


class ImportTx(object):
    def __init__(self, parsed_tx):
        self._parsed_tx = parsed_tx
        self._processed = False
        self._category = u''

    @property
    def parsed_tx(self):
        return self._parsed_tx

    @property
    def processed(self):
        return self._processed

    @processed.setter
    def processed(self, value):
        self._processed = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value
