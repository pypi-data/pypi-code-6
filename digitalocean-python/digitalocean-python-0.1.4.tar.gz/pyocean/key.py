# encoding: utf-8

from .base import Resource, ResourceIterator


class Key(Resource):
    """This class represents the SSH key object.
    """

    def __init__(self, attrs={}):
        super(Key, self).__init__(attrs)
        self._resource = 'account/keys'
        self._json_key = 'ssh_key'

    def rename(self, name):
        path = '%s/%s' % (self._resource, str(self.id))
        data = self.call_api(path, method='put', data={'name': name})
        self._attrs = data[self._json_key]
        return self

    def delete(self):
        return self.destroy()

    def __str__(self):
        return "<SSH Key '%s' (%s)>" % (self.name, self.fingerprint)


class KeyIterator(ResourceIterator):
    """This class represents collections of SSH keys.
    """

    def __init__(self):
        super(KeyIterator, self).__init__()
        self._resource = 'account/keys'
        self._json_key = 'ssh_keys'
