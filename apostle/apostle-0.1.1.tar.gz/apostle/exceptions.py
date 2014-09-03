class BaseApostleError(Exception):
    """
    Base class for all Apostle errors.
    """

    def __init__(self, message):
        super(BaseApostleError, self).__init__()
        self._message = message

    def __str__(self):
        # all sub-classes should set self._message in their initializers
        return self._message


class DeliveryError(BaseApostleError): pass
class UnauthorizedError(BaseApostleError): pass
class ForbiddenError(BaseApostleError): pass
class ServerError(BaseApostleError): pass
class UnprocessableEntityError(BaseApostleError): pass
class ValidationError(BaseApostleError): pass
