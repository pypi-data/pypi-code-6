import re

from flask import request


class Forbidden(Exception):
    pass


class UnAuthorized(Exception):
    pass


class Authorization(object):
    def authorize(self, resource):
        try:
            func = getattr(self, request.method.lower())
        except:
            func = self.default

        if not func(resource):
            raise Forbidden('Access Denied')

    def default(self, resource):
        pass
