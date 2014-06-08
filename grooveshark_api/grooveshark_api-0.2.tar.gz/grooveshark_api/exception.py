# coding: utf-8


class InvalidArgumentValueException(Exception):
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidCredentialsException(Exception):
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RequestErrorException(Exception):
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)
