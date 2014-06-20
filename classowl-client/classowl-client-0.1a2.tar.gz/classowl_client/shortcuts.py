class LazyResource(object):
    """
    endpoint that is first instantiated on use
    """
    _client = None

    @classmethod
    def _get_client(cls):
        if cls._client is None:
            from classowl_client import username, password, client
            cls._client = client.create_client(username, password)
        return cls._client

    @property
    def _resource(self):
        return getattr(self._get_client(), self._endpoint)

    def __init__(self, endpoint):
        self._endpoint = endpoint

    def __getattr__(self, name):
        return getattr(self._resource, name)

    def __call__(self, *args, **kwargs):
        return self._resource(*args, **kwargs)
