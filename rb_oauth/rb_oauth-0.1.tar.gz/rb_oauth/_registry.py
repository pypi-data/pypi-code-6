"""Generic registry helpers."""

class Registry(object):

    ON_COLLISION = ['fail', 'overwrite', 'ignore']

    def __init__(self, oncollision=None):
        if oncollision is None:
            oncollision = self.ON_COLLISION[0]
        elif oncollision not in self.ON_COLLISION:
            raise ValueError('unrecognized oncollision value: {!r}'
                             .format(oncollision))
        self._oncollision = oncollision
        self._raw = {}

    def __len__(self):
        return len(self._raw)

    def __iter__(self):
        for key in self._raw:
            yield key

    def __getitem__(self, key):
        return self._raw[key]

    @property
    def oncollision(self):
        return self._oncollision

    def register(self, cls, name=None):
        """Register a Provider subclass.

        This method may be used as a class decorator.

        """
        if name is None:
            try:
                name = cls.NAME
            except AttributeError:
                raise ValueError('missing name')

        if name in self._raw:
            if self.oncollision == 'fail':
                raise KeyError('name already registered: {!r}'.format(name))
            elif self.oncollision == 'overwrite':
                pass
            elif self.oncollision == 'ignore':
                name = None
            else:
                raise NotImplementedError

        if name is not None:
            self._raw[name] = cls
        return cls
