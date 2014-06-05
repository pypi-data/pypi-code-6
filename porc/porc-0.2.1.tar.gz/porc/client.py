from . import resource
from . import collection


class Client(resource.Resource):

    """
    The top-level resource for interacting with Orchestrate.
    Handles authentication, spawns collections.

    ```
    client = porc.Client(API_KEY)
    client.ping().result().raise_for_status()
    # if it throws an error, you're not authenticated
    ```
    """

    def __init__(self, api_key, api_version=0, **kwargs):
        uri = 'https://%s:@api.orchestrate.io/v%d' % (api_key, api_version)
        super(Client, self).__init__(uri, **kwargs)

    def collection(self, name, **kwargs):
        """
        Spawns a collection object, inheriting options from the client object.
        Note that this does not create a collection in Orchestrate.
        """
        return self._init_child(collection.Collection, name, **kwargs)

    def ping(self):
        """
        Sends Orchestrate a HEAD request to determine
        connectivity and authentication.
        """
        return self.head()
