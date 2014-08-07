class PayzoneError(Exception):
    pass


class MissingParameterError(PayzoneError):
    pass


class PayzoneAPIError(PayzoneError):
    """ For errors raised from api.payzone.ma
    """
    pass
