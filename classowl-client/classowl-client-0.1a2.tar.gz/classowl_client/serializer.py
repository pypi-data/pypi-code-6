import slumber
import urlparse
import collections
from pprint import pformat


class Serializer(slumber.Serializer):
    def set_client(self, client):
        """
        api client needed to turn uris to usable endpoints
        """
        self._client = client

    def get_serializer(self, name=None, content_type=None):
        """nicely wrap serializers"""
        return SerializerWrapper(super(Serializer, self).get_serializer(name, content_type),
                                 self._client)


class SerializerWrapper(slumber.serialize.BaseSerializer):
    """
    turns dictionary data into objects and vice versa
    """
    _serializer = None
    _client = None

    def __init__(self, serializer, client):
        self._serializer = serializer
        self._client = client
        self.content_types = serializer.content_types
        self.key = serializer.key

    def get_content_type(self):
        return self._serializer.get_content_type()

    def loads(self, data):
        return DataObject(self._client, **self._serializer.loads(data))

    def dumps(self, data):
        return self._serializer.dumps(data._data if isinstance(data, DataObject) else data)


class DataObject(collections.Mapping):
    """
    object that allows the data to be accessed as attributes
    and turns all uri fields into usable api endpoints
    """
    def __init__(self, client, **kwargs):
        self._client = client
        self._data = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return 'DataObject(**%s)' % pformat(self._data)

    def __str__(self):
        return str(self._data)

    def __setattr__(self, name, value):
        if not name.startswith('_') and name in self._data:
            self._data[name] = value
            value = _unpack(value, self._client)
        super(DataObject, self).__setattr__(name, value)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)


def _unpack(value, client):
    if isinstance(value, dict):
        return DataObject(client, **value)
    elif isinstance(value, list):
        return [_unpack(item, client) for item in value]
    elif isinstance(value, basestring):
        return resourcify(value, client)
    else:
        return value


def resourcify(value, client):
    """
    turn an uri to a usable api endpoint
    """
    client_url = urlparse.urlsplit(client._store['base_url'])
    if client_url.path not in value:
        return value
    resource_url = urlparse.urlsplit(value)
    new_url = urlparse.urlunsplit((client_url.scheme,
                                   client_url.netloc,
                                   resource_url.path,
                                   resource_url.query,
                                   resource_url.fragment))
    kwargs = client._store.copy()
    kwargs.update({'base_url': new_url})
    if resource_url.query or resource_url.fragment:
        kwargs.update({'append_slash': False})
    return slumber.Resource(**kwargs)
