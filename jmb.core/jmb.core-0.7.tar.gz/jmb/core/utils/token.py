# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.hashcompat import sha_constructor


class TokenGenerator(object):
    def make_token(self, code):
        token = sha_constructor(
            settings.SECRET_KEY
            + unicode(code)
        ).hexdigest()[::2]
        return token

    def check_token(self, code, token, duration=None):
        if token == self.make_token(code):
            return True
        return False
