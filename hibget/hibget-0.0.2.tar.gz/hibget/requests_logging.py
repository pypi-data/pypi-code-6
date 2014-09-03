__author__ = "Joel Pedraza"
__copyright__ = "Copyright 2014, Joel Pedraza"
__license__ = "MIT"
__all__ = ['RequestsFormatter', 'format_request', 'format_response']

from logging import Formatter
from requests import RequestException


class RequestsFormatter(Formatter):
    def format(self, record):
        if isinstance(record.msg, RequestException):
            e = record.msg
            msg = format_request(e.request)
            if e.response is not None:
                msg += format_response(e.response)
            record.msg = "\n".join([msg, str(e)])

        return super(RequestsFormatter, self).format(record)


def format_request(request):
    s = ["HTTP/1.1 %s %s" % (request.method, request.url),
         _prefix_join(request.headers)]
    if request.body:
        s += ['\n', request.body, '\n']
    return "".join(s)


def format_response(response):
    request = response.request
    s = ["HTTP/1.1 %s %s %d %s" % (request.method, response.url, response.status_code, response.reason),
         _prefix_join(response.headers)]
    if response.text:
        s += ['\n', response.text, '\n']
    return "".join(s)


def _prefix_join(data, width=4, fillchar=" "):
    prefix = "\n" + "".ljust(width, fillchar)
    try:
        return "".join(["%s%s: %s" % (prefix, k, v) for k, v in data.items()])
    except AttributeError:
        pass

    if isinstance(data, list):
        return "".join(["%s%s" % (prefix, v) for v in data])

    return prefix + str(data)