class Field(object):

    def __init__(self, length, required=True, default=None):
        self.name = None
        self.required = required
        self.length = length
        self.default = default

    def __get__(self, inst, cls):
        if inst is None:
            return self
        assert self.name is not None
        return inst.__getattr__(self.name)

    def __set__(self, inst, value):
        assert self.name is not None
        if inst._values is None:
            inst._values = {}
        value = self.convert(value)
        self.check(value)
        inst._values[self.name] = value

    def convert(self, value):
        if value is None:
            value = ''
        if not isinstance(value, unicode):
            value = unicode(value)
        return value

    def check(self, value):
        if len(value) > self.length:
            raise ValueError('Value %s is too long for field %s '
                '(maximum %s)' % (value, self.name, self.length))


class AlphaNumeric(Field):

    def __init__(self, length, clipping=False, **kwargs):
        super(AlphaNumeric, self).__init__(length, **kwargs)
        self.clipping = clipping

    def convert(self, value):
        value = super(AlphaNumeric, self).convert(value)
        if self.clipping:
            value = value[:self.length]
        value = value.ljust(self.length)
        return value

    def check(self, value):
        try:
            super(AlphaNumeric, self).check(value)
        except ValueError:
            if not self.clipping:
                raise


class Numeric(Field):

    def convert(self, value):
        value = super(Numeric, self).convert(value)
        if not value:
            value = ''.ljust(self.length)
        else:
            value = value.zfill(self.length)
        return value

    def check(self, value):
        super(Numeric, self).check(value)
        value = value.strip()
        if value and not value.isdigit():
            raise ValueError('Value %s on field %s is no numeric value' %
                (value, self.name))


class Currency(Field):

    def convert(self, value):
        value = super(Currency, self).convert(value)
        value = value.ljust(self.length)
        value = value.replace('.', ',')
        return value


class Date(Field):

    def __init__(self, **kwargs):
        super(Date, self).__init__(6, **kwargs)

    def convert(self, value):
        if value is None:
            value = ''.ljust(self.length)
        elif not isinstance(value, str):
            value = value.strftime('%y%m%d')
        return value
