# exceptions for access to the Mirador API
# subclassing appropriate exceptions for function
from httplib import HTTPException
from collections import defaultdict


class MiradorException(HTTPException):
    code = 500

    def __init__(self, *args, **kwargs):
        code = kwargs.get('code', self.code)
        super(MiradorException, self).__init__(
            "[{code}]: {message}".format(
                message=" ".join(map(str, args)), code=code
            )
        )


class InvalidRequestException(MiradorException):
    code = 400

    def __init__(self, *args, **kwargs):
        super(InvalidRequestException, self).__init__(
            "must include valid URL or file"
        )


class UnauthorizedException(MiradorException):
    code = 403

    def __init__(self, *args, **kwargs):
        super(UnauthorizedException, self).__init__(
            "API key is invalid. Contact support@mirador.im for valid key"
        )


class TimeoutException(MiradorException):
    code = 408

    def __init__(self, *args, **kwargs):
        super(TimeoutException, self).__init__(
            "Timeout occurred in request. Adjust MiradorClient.TIMEOUT or try request again"
        )


def default_exception():
    return MiradorException


http_exceptions = defaultdict(default_exception)
http_exceptions[400] = InvalidRequestException
http_exceptions[403] = UnauthorizedException
http_exceptions[408] = TimeoutException
http_exceptions[500] = MiradorException
