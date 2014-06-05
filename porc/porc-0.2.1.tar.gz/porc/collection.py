from . import resource
from . import key
from . import page


class Collection(resource.Resource):

    """
    From the Orchestrate docs:
    
    "Collections are groupings of the JSON objects. 
    Collections are analogous to tables in a relational database."

    The collection object performs searches over the JSON objects stored in a collection, 
    and can spawn key objects representing JSON objects.

    ```python
    collection = porc.Client(API_KEY).collection(NAME)
    for page in collection.search({"query": "cool_*"}):
        print page.json()
        # {
        #     "count": 1,
        #     "next": "/v0/collection?limit=10&query=test&offset=1",
        #     "prev": "/v0/collection?limit=10&query=test&offset=0",
        #     "results": [
        #         {
        #             "path": {
        #                 "collection": "neat_stuff",
        #                 "key": "cool_beans",
        #                 "ref": "20c14e8965d6cbb0"
        #             },
        #             "score": 1.0,
        #             "value": {
        #                 "coolness": 999
        #             }
        #         }
        #     ],
        #     "total_count": 100
        # }
    ```
    """

    def key(self, name, **kwargs):
        """
        Spawns a key object, inheriting options from the collection object.
        Note that this does not create a key in Orchestrate.
        """
        return self._init_child(key.Key, name, **kwargs)

    def list(self, **kwargs):
        """
        Returns a page object to page through list results.
        """
        return page.Page(self.uri, kwargs, session=self._session, **self.opts)

    def search(self, **kwargs):
        """
        Returns a page object to page through search results.

        Alias to `self.list`.
        """
        return self.list(**kwargs)

    def delete(self, querydict={}, **headers):
        """
        Deletes a collection and all the keys it contains.
        Automatically sets `?force=true` in the querystring.
        """
        querydict['force'] = True
        return super(Collection, self).delete(querydict, **headers)
