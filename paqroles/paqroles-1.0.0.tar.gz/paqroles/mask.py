class Mask(str):
    def __new__(cls, value):
        if isinstance(value, Mask):
            return value
        obj = str.__new__(cls, value.replace(':', '.'))
        return obj


    def __add__(self, other):
        return Mask('{}.{}'.format(str(self).rstrip('.'), str(other).lstrip('.')))


    def __radd__(self, other):
        return Mask('{}.{}'.format(str(other).rstrip('.'), str(self).lstrip('.')))


    def allows(self, other):
        return (str(other) + '.').startswith(str(self) + '.')
