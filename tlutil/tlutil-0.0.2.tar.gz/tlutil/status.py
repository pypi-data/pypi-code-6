# -*- coding: utf-8 -*-
"""
    tlutil.status
"""


__all__ = [
    "status_text", "is_informational", "is_success",
    "is_redirect", "is_client_error", "is_server_error"
]

STATUS_CONTINUE = 100
STATUS_SWITCHING_PROTOCOLS = 101

STATUS_OK = 200
STATUS_CREATED = 201
STATUS_ACCEPTED = 202
STATUS_NON_AUTHORITATIVE_INFO = 203
STATUS_NO_CONTENT = 204
STATUS_RESET_CONTENT = 205
STATUS_PARTIAL_CONTENT = 206

STATUS_MULTIPLE_CHOICES = 300
STATUS_MOVED_PERMANENTLY = 301
STATUS_FOUND = 302
STATUS_SEE_OTHER = 303
STATUS_NOT_MODIFIED = 304
STATUS_USE_PROXY = 305
STATUS_TEMPORARY_REDIRECT = 307

STATUS_BAD_REQUEST = 400
STATUS_UNAUTHORIZED = 401
STATUS_PAYMENT_REQUIRED = 402
STATUS_FORBIDDEN = 403
STATUS_NOT_FOUND = 404
STATUS_METHOD_NOT_ALLOWED = 405
STATUS_NOT_ACCEPTABLE = 406
STATUS_PROXY_AUTH_REQUIRED = 407
STATUS_REQUEST_TIMEOUT = 408
STATUS_CONFLICT = 409
STATUS_GONE = 410
STATUS_LENGTH_REQUIRED = 411
STATUS_PRECONDITION_FAILED = 412
STATUS_REQUEST_ENTITY_TOO_LARGE = 413
STATUS_REQUEST_URI_TOO_LONG = 414
STATUS_UNSUPPORTED_MEDIA_TYPE = 415
STATUS_REQUESTED_RANGE_NOT_SATISFIABLE = 416
STATUS_EXPECTATION_FAILED = 417
STATUS_TEAPOT = 418

STATUS_INTERNAL_SERVER_ERROR = 500
STATUS_NOT_IMPLEMENTED = 501
STATUS_BAD_GATEWAY = 502
STATUS_SERVICE_UNAVAILABLE = 503
STATUS_GATEWAY_TIMEOUT = 504
STATUS_HTTP_VERSION_NOT_SUPPORTED = 505

STATUS_PRECONDITION_REQUIRED = 428
STATUS_TOO_MANY_REQUESTS = 429
STATUS_REQUEST_HEADER_FIELDS_TOO_LARGE = 431
STATUS_NETWORK_AUTHENTICATION_REQUIRED = 511


STATUS_TEXT = {
    STATUS_CONTINUE: "Continue",
    STATUS_SWITCHING_PROTOCOLS: "Switching Protocols",

    STATUS_OK: "OK",
    STATUS_CREATED: "Created",
    STATUS_ACCEPTED: "Accepted",
    STATUS_NON_AUTHORITATIVE_INFO: "Non-Authoritative Information",
    STATUS_NO_CONTENT: "No Content",
    STATUS_RESET_CONTENT: "Reset Content",
    STATUS_PARTIAL_CONTENT: "Partial Content",

    STATUS_MULTIPLE_CHOICES: "Multiple Choices",
    STATUS_MOVED_PERMANENTLY: "Moved Permanently",
    STATUS_FOUND: "Found",
    STATUS_SEE_OTHER: "See Other",
    STATUS_NOT_MODIFIED: "Not Modified",
    STATUS_USE_PROXY: "Use Proxy",
    STATUS_TEMPORARY_REDIRECT: "Temporary Redirect",

    STATUS_BAD_REQUEST: "Bad Request",
    STATUS_UNAUTHORIZED: "Unauthorized",
    STATUS_PAYMENT_REQUIRED: "Payment Required",
    STATUS_FORBIDDEN: "Forbidden",
    STATUS_NOT_FOUND: "Not Found",
    STATUS_METHOD_NOT_ALLOWED: "Method Not Allowed",
    STATUS_NOT_ACCEPTABLE: "Not Acceptable",
    STATUS_PROXY_AUTH_REQUIRED: "Proxy Authentication Required",
    STATUS_REQUEST_TIMEOUT: "Request Timeout",
    STATUS_CONFLICT: "Conflict",
    STATUS_GONE: "Gone",
    STATUS_LENGTH_REQUIRED: "Length Required",
    STATUS_PRECONDITION_FAILED: "Precondition Failed",
    STATUS_REQUEST_ENTITY_TOO_LARGE: "Request Entity Too Large",
    STATUS_REQUEST_URI_TOO_LONG: "Request URI Too Long",
    STATUS_UNSUPPORTED_MEDIA_TYPE: "Unsupported Media Type",
    STATUS_REQUESTED_RANGE_NOT_SATISFIABLE: "Requested Range Not Satisfiable",
    STATUS_EXPECTATION_FAILED: "Expectation Failed",
    STATUS_TEAPOT: "I'm a teapot",

    STATUS_INTERNAL_SERVER_ERROR: "Internal Server Error",
    STATUS_NOT_IMPLEMENTED: "Not Implemented",
    STATUS_BAD_GATEWAY: "Bad Gateway",
    STATUS_SERVICE_UNAVAILABLE: "Service Unavailable",
    STATUS_GATEWAY_TIMEOUT: "Gateway Timeout",
    STATUS_HTTP_VERSION_NOT_SUPPORTED: "HTTP Version Not Supported",

    STATUS_PRECONDITION_REQUIRED: "Precondition Required",
    STATUS_TOO_MANY_REQUESTS: "Too Many Requests",
    STATUS_REQUEST_HEADER_FIELDS_TOO_LARGE: "Request Header Fields Too Large",
    STATUS_NETWORK_AUTHENTICATION_REQUIRED: "Network Authentication Required",
}


def status_text(code):
    return STATUS_TEXT[code]


def is_informational(code):
    if code >= 100 and code < 200:
        return True
    return False


def is_success(code):
    if code >= 200 and code < 300:
        return True
    return False


def is_redirect(code):
    if code >= 300 and code < 400:
        return True
    return False


def is_client_error(code):
    if code >= 400 and code < 500:
        return True
    return False


def is_server_error(code):
    if code >= 500 and code < 600:
        return True
    return False
