from .error import ApiError as RootError
from . import data_types

class InvalidRequestError(RootError):
    def __init__(self, status, raw_data):
        data = data_types.ErrorData(raw_data)
        RootError.__init__(self, '%s: %s' % ('InvalidRequestError', data.error.message))
        self.status = status
        self.data = data

class AuthenticationError(RootError):
    def __init__(self, status, raw_data):
        data = data_types.ErrorData(raw_data)
        RootError.__init__(self, '%s: %s' % ('AuthenticationError', data.error.message))
        self.status = status
        self.data = data

class CardError(RootError):
    def __init__(self, status, raw_data):
        data = data_types.ErrorData(raw_data)
        RootError.__init__(self, '%s: %s' % ('CardError', data.error.message))
        self.status = status
        self.data = data

class ApiError(RootError):
    def __init__(self, status, raw_data):
        data = data_types.ErrorData(raw_data)
        RootError.__init__(self, '%s: %s' % ('ApiError', data.error.message))
        self.status = status
        self.data = data

