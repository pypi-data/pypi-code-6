# Exceptions/Errors
ERRORS = {
    'InvalidURL': 1,
    'RequestError': 4,  # 4xx errors
    'ServerError': 5    # 5xx errors
}


class InvalidURLError(Exception):
    pass


class RequestError(Exception):
    def __init__(self, code, body):
        self.code = code
        self.body = body

    def __cmp__(self, other):
        if self.code == other:
            return 0
        return 1 if self.code > other else -1

    def __str__(self):
        return self.body


class ServerError(Exception):
    def __init__(self, code, body):
        self.code = code
        self.body = body

    def __cmp__(self, other):
        if self.code == other:
            return 0
        return 1 if self.code > other else -1

    def __str__(self):
        return self.body
