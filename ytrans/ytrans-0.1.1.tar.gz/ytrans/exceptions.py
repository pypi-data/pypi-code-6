# coding: utf-8


class KeyNotFound(Exception):
    def __init__(self):
        super(KeyNotFound, self).__init__("API Key not found!")


class APIException(Exception):
    """
    Base class for all API Exceptions
    """
    message = None

    def __init__(self):
        assert self.message is not None
        super(APIException, self).__init__(self.message)


class InvalidKeyError(APIException):
    message = "Invalid API key."


class KeyBlockedError(APIException):
    message = "This API key has been blocked."


class DailyReqLimitExceededError(APIException):
    message = ("You have reached the daily limit"
               " for requests (including calls of the translate method).")


class DailyCharLimitExceededError(APIException):
    message = ("You have reached the daily limit for the "
               "volume of translated text (including calls"
               " of the translate method).")


class TextTooLongError(APIException):
    message = "The text size exceeds the maximum."


class UnprocessableTextError(APIException):
    message = "The text could not be translated. "


class LangNotSupportedError(APIException):
    message = "The specified translation direction is not supported."


# code -> exception mapping
exception_map = {
    401: InvalidKeyError,
    402: KeyBlockedError,
    403: DailyReqLimitExceededError,
    404: DailyCharLimitExceededError,
    413: TextTooLongError,
    422: UnprocessableTextError,
    501: LangNotSupportedError
}


def throw(code):
    """
    Throws exception with code ``code``

    :param int code: Error code
    """
    assert code in exception_map
    raise exception_map[code]
