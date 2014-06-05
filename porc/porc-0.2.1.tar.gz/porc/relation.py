from .resource import Resource
from .page import Page


class Relation(Resource):

    """
    From the Orchestrate docs:

    "The Graph functionality allows for directed relations 
    to be created between collection/key pairs 
    and for those relations to be traversed."

    A relation object allows you to create, delete, and query
    relations associated with a key.

    ```python
    relation = key.relation()
    # create
    response = relation.put('loves', 'people', 'David Bowie').result()
    response.raise_for_status()
    # query
    response = relation.get('loves')
    response.raise_for_status()
    print response.json()
    # {
    #     "count": 1,
    #     "results": [
    #         {
    #             "path": {
    #                 "collection": "people",
    #                 "key": "David Bowie",
    #                 "ref": "0acfe7843316529f"
    #             },
    #             "value": {
    #                 "age": 67,
    #                 "name": "David Bowie"
    #             }
    #         }
    #     ]
    # }
    # delete
    response = relation.delete('loves', 'people', 'David Bowie').result()
    response.raise_for_status()
    ```
    """

    def __init__(self, uri, **kwargs):
        self._root_url = uri
        super(Relation, self).__init__(uri, **kwargs)

    def get(self, *relations, **headers):
        """
        Queries all relations specified in `relations`, ex:

            relation.get('friend', 'friend')

        ...would return all friends of friends.

        N.B.: Graph query results are not currently paginated.
        """
        resource = self._init_child(Resource, 'relations', *relations)
        return resource.get(**headers)

    def put(self, relation, collection, key, **headers):
        """
        Creates a relationship between two objects.
        Relations can span collections.
        """
        resource = self._init_child(Resource, 'relation', relation, collection, key)
        return resource.put(**headers)

    def delete(self, relation, collection, key, querydict={}, **headers):
        """
        Deletes a relationship between two objects.
        Automatically sets `?purge=true` in the querystring.
        """
        resource = self._init_child(Resource, 'relation', relation, collection, key)
        querydict['purge'] = True
        return resource.delete(querydict, **headers)
