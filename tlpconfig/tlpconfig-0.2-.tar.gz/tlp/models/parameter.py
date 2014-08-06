class Parameter:
    def __init__(self, name):
        self.active = False
        self.name = name
        self._value = ''
        self.initial_state = {}

    def is_changed(self):
        start_active = self.initial_state['active']
        start_value = self.initial_state['value']
        active = self.active
        value = self._value

        return active != start_active or (active and value != start_value)

    def write(self, configuration):
        template = '{0}={1}'
        current = template.format(self.name, self.initial_state['value'])
        new = template.format(self.name, self._value)

        if not self.active:
            new = '#' + new

        if not self.initial_state['active']:
            current = '#' + current

        return configuration.replace(current, new)


class TextParameter(Parameter):
    def __init__(self, name, quotes=''):
        Parameter.__init__(self, name)
        self.quotes = quotes

    @property
    def value(self):
        return self._value.strip().replace(self.quotes, '')

    @value.setter
    def value(self, value):
        self._value = '{0}{1}{0}'.format(self.quotes, value.strip())


class ListParameter(Parameter):
    @property
    def value(self):
        return self._value.strip().replace('"', '').split(' ')

    @value.setter
    def value(self, value):
        self._value = '"{0}"'.format(' '.join(value))


class BooleanParameter(Parameter):
    def __init__(self, name, yes='1', no='0'):
        Parameter.__init__(self, name)
        self.yes = yes
        self.no = no

    @property
    def value(self):
        return self._value.strip() == self.yes

    @value.setter
    def value(self, value):
        self._value = self.yes if value else self.no


class NumericParameter(Parameter):
    @property
    def value(self):
        return float(self._value)

    @value.setter
    def value(self, value):
        self._value = str(value).replace('.0', '')
