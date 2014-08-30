from .indices import IndexManager
from whoosh.qparser import MultifieldParser


class Searcher(object):
    def __init__(self):
        self.index = IndexManager().get()

    def search(self, string, limit=25, **kwargs):
        fields = [u"name", u"comment", u"product", u"categories"]
        qp = MultifieldParser(
            fields,
            self.index.schema,
            fieldboosts={u"name": 5., u"categories": 2., u"product": 3.}
        )
        with self.index.searcher() as searcher:
            results = [
                dict(obj.iteritems())
                for obj in searcher.search(qp.parse(string), limit=limit)
            ]
        return results
