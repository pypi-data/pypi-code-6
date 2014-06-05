from .resource import Resource
from .page import Page
from .util import create_timestamp
from datetime import datetime

class Event(Resource):

    """
    From the Orchestrate docs:

    "Events are a way to associate time-ordered data with a key."

    The event object allows you to create, read, update, and delete
    different events, and to perform queries over events associated
    with a key.

    ```python
    event = key.event(TYPE)
    # create
    response = event.post({"msg": "hello world, again"}).result()
    timestamp = response.path['timestamp']
    ordinal = response.path['ordinal']
    response.raise_for_status()
    # read
    response = event.get(timestamp, ordinal).result()
    response.raise_for_status()
    print response.json()
    # {
    #     "path": {
    #         "collection": "asdf",
    #         "key": "key",
    #         "ref": "ae3dfa4325abe21e",
    #         "type": "played",
    #         "timestamp": 1369832019085,
    #         "ordinal": 9
    #     },
    #     "value": {
    #       "msg": "hello world, again"
    #     },
    #     "timestamp": 1369832019085,
    #     "ordinal": 9
    # }
    # update
    response = event.put(timestamp, ordinal, {"msg": "goodnight moon"}).result()
    response.raise_for_status()
    # query
    for page in event.list():
        print page.json()
        # {
        #   "results": [
        #     {
        #       "path": {
        #         "collection": "collection",
        #         "key": "key",
        #         "type": "type",
        #         "timestamp": 1369832019085,
        #         "ordinal": 9,
        #         "ref": "ae3dfa4325abe21e"
        #       },
        #       "value": {
        #         "msg": "goodnight moon"
        #       },
        #       "timestamp": 1369832019085,
        #       "ordinal": 9
        #     }
        #   "count": 1
        # }
    # delete
    response = event.delete(timestamp, ordinal).result()
    response.raise_for_status()
    ```
    """

    def get(self, timestamp=None, ordinal=None, querydict={}, **headers):
        """
        Retrieves a given event. 
        If timestamp is a datetime object, 
        it will be converted to milliseconds since epoch.
        """
        if not timestamp and not ordinal:
            return self.list(querydict, **headers)
        else:
            if type(timestamp) == datetime:
                timestamp = create_timestamp(timestamp)
            resource = self._init_child(Resource, str(timestamp), ordinal)
            return resource.get(**headers)

    def post(self, body, timestamp=None, **headers):
        """
        Creates a new event.
        If timestamp is not provided, Orchestrate will give it one.
        """
        if timestamp:
            if type(timestamp) == datetime:
                timestamp = create_timestamp(timestamp)
            resource = self._init_child(Resource, str(timestamp))
        else:
            resource = self._init_child(Resource)

        return resource.post(body, **headers)

    def put(self, timestamp, ordinal, body, **headers):
        """
        Updates a given event.
        If timestamp is a datetime object, 
        it will be converted to milliseconds since epoch.
        """
        if type(timestamp) == datetime:
            timestamp = create_timestamp(timestamp)
        resource = self._init_child(Resource, str(timestamp), ordinal)
        return resource.put(body, **headers)

    def delete(self, timestamp, ordinal, querydict={}, **headers):
        """
        Deletes a given event.
        Automatically sets `?purge=true` in the querystring.
        """
        if type(timestamp) == datetime:
            timestamp = create_timestamp(timestamp)
        resource = self._init_child(Resource, str(timestamp), ordinal)
        querydict['purge'] = True
        return resource.delete(querydict, **headers)

    def list(self, querydict, **headers):
        """
        Returns a page representing a given query of events.
        See `Page` for more details on the page object.
        """
        return Page(self.uri, querydict, session=self._session, headers=headers)
