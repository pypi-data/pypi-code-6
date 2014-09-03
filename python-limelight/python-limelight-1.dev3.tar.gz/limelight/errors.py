# -*- coding: utf-8 -*-


class LimeLightException(Exception):
    pass


class ImproperlyConfigured(LimeLightException):
    pass


class RequestError(LimeLightException):
    pass


class NoPreviousOrder(LimeLightException):
    pass


class TransactionDeclined(LimeLightException):
    pass


class ValidationError(LimeLightException):
    pass