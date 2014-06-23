class Field(object):

    def __init__(self, length, required=True, default=None, clipping=False):
        self.name = None
        self.required = required
        self.length = length
        self.default = default
        self.clipping = clipping

    def __get__(self, inst, cls):
        if inst is None:
            return self
        assert self.name is not None
        return inst.__getattr__(self.name)

    def __set__(self, inst, value):
        assert self.name is not None
        if inst._values is None:
            inst._values = {}
        inst._values[self.name] = value


class AlphaNumeric(Field):

    def __get__(self, inst, cls):
        value = super(AlphaNumeric, self).__get__(inst, cls)
        if not isinstance(value, AlphaNumeric):
            if value is None:
                value = ''
            value = str(value).ljust(self.length)
        return value

    def __set__(self, inst, value):
        if value:
            length = len(str(value))
            if length > self.length:
                if self.clipping:
                    value = value[:self.length]
                else:
                    raise ValueError('Value %s is too long for field %s '
                        '(maximum %s)' % (value, self.name, self.length))
        super(AlphaNumeric, self).__set__(inst, value)


class Numeric(AlphaNumeric):

    def __get__(self, inst, cls):
        value = Field.__get__(self, inst, cls)
        if not isinstance(value, Numeric):
            if value is None:
                value = ''.ljust(self.length)
            else:
                value = str(value).zfill(self.length)
        return value

    def __set__(self, inst, value):
        if value:
            if not str(value).isdigit():
                raise ValueError('Value %s on field %s is no numeric value' %
                    (value, self.name))
        super(Numeric, self).__set__(inst, value)


class Currency(AlphaNumeric):

    def __get__(self, inst, cls):
        value = super(Currency, self).__get__(inst, cls)
        if not isinstance(value, Currency):
            if value is None:
                value = ''.ljust(self.length)
            else:
                value = str(value).replace('.', ',')
        return value


class Date(Field):

    def __init__(self, required=True):
        super(Date, self).__init__(6, required=required)

    def __get__(self, inst, cls):
        value = super(Date, self).__get__(inst, cls)
        if not isinstance(value, Date):
            if value is None:
                value = ''.ljust(self.length)
            else:
                value = value.strftime('%y%m%d')
        return value
