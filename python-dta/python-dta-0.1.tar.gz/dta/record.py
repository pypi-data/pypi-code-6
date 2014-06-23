import fields


class DTARecord(object):

    def __init__(self):
        cls = self.__class__
        cls._fields = {}
        self._values = None
        for attr in dir(cls):
            if isinstance(getattr(cls, attr), fields.Field):
                cls._fields[attr] = getattr(cls, attr)

        for name, field in cls._fields.iteritems():
            field.name = name
            setattr(self, name, field.default)

    def __getattr__(self, name):
        if self._values and name in self._values:
            return self._values.get(name)
        raise AttributeError("Record '%s' has no attribute '%s': %s"
            % (self, name, self._values))

    def check(self):
        for name, field in self._fields.items():
            if field.required and not getattr(self, name).strip():
                raise DTAValueError('Field %s is required' % field.name)

    def generate(self):
        self.check()


class DTAValueError(Exception):
    pass
