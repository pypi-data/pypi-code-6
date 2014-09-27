# encoding: utf-8

class DOException(Exception):
    """Base exception for pyocean package.
    """

    def __init__(self, msg=None, code=None):
        super(DOException, self).__init__(msg)
        self.message = msg
        self.code = code


class ClientError(DOException):
    """Raised when received HTTP 4xx error.
    """
    pass

class ServerError(DOException):
    """Raised when received HTTP 5xx error.
    """
    pass

class AuthException(DOException):
    """Raised when received HTTP 401 Unauthorized error.
    """
    pass

class InvalidResponse(DOException):
    """Raised when retrieved invalid JSON response.
    """
    pass

class DropletActionError(DOException):
    """Raised when a droplet action (reboot, rebuild, etc) is failed.
    """
    pass

class ImageActionError(DOException):
    """Raised when an image action (rename, transfer) is failed.
    """
    pass
