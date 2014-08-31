from urllib import urlencode


def entity_retriever(path, available_includes=frozenset()):
    @property
    def retriever(self):
        return BoundEntityRetriever(
            client=self, path=path, available_includes=available_includes,
        )
    return retriever


class BoundEntityRetriever(object):
    def __init__(self, client, path, available_includes):
        self.available_includes = available_includes
        self.client = client
        self.path = path

    def lookup(self, mbid, include=()):
        """
        Lookup an entity directly from a specified :term:`MBID`\ .

        """

        if include:
            for included in include:
                if included not in self.available_includes:
                    raise ValueError(
                        "{0!r} is not an includable entity for {1}".format(
                            included, self.path,
                        ),
                    )
            query_string = "?" + urlencode([("inc", " ".join(include))])
        else:
            query_string = ""

        path = "{0}/{1}{2}".format(self.path, mbid, query_string)
        return self.client.request(path)

    def search(self, query):
        return self.client.request(self.path + "?query=" + query)
