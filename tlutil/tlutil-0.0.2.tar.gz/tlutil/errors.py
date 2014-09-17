# -*- coding: utf-8 -*-
"""
    tlutil.errors
"""

import status


__all__ = [
    "AppError", "ClientError", "ServerError"
]


class AppError(Exception):

    def __init__(self, code, message, status_code):
        self.code = code
        self.message = message
        self.status_code = status_code

    def __str__(self):
        message = self.message
        if isinstance(message, unicode):
            message = message.encode('utf-8')
        return '<%d %s>' % (self.code, message)


class ClientError(AppError):

    def __init__(self, code, message,
                 status_code=status.STATUS_BAD_REQUEST):
        super(ClientError, self).__init__(code, message, status_code)


class ServerError(AppError):

    def __init__(self, code, message,
                 status_code=status.STATUS_INTERNAL_SERVER_ERROR):
        super(ServerError, self).__init__(code, message, status_code)
