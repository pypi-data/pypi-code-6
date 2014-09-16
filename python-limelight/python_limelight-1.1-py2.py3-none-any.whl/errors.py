# -*- coding: utf-8 -*-


class LimeLightException(Exception):
    pass


class ImproperlyConfigured(LimeLightException):
    pass


# noinspection PyShadowingBuiltins
class ConnectionError(LimeLightException):
    pass


class NoPreviousOrder(LimeLightException):
    pass


class TransactionDeclined(LimeLightException):
    pass


class CouldNotFindProspectRecord(LimeLightException):
    pass


class ValidationError(LimeLightException):
    pass