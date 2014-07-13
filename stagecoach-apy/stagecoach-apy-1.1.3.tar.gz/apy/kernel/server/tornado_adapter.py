import json
import sys
import traceback
import logging
import six
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from apy.http import Request
from apy.kernel.server.base_adapter import BaseServerAdapter


class MainHandler(RequestHandler):
    dispatcher = None
    error_handler = None

    def _execute(self, transforms, *args, **kwargs):
        self._transforms = transforms
        self.path_args = [self.decode_argument(arg) for arg in args]
        self.path_kwargs = dict((k, self.decode_argument(v, name=k))
                                for (k, v) in kwargs.items())
        self._when_complete(self.prepare(), self._execute_method)

    def _execute_method(self):
        if not self._finished:
            self._when_complete(self._serve(), self._execute_finish)

    def get_request(self):
        path = self.request.path
        method = self.request.method

        query = parse_string(self.request.query)
        headers = self.request.headers

        data = {}

        try:
            body_content = get_body_content_from_request_body(self.request.body)
            if body_content:
                if 'Content-Type' in headers:
                    content_type = headers['Content-Type']
                    if content_type.startswith('application/json'):
                        data = json.loads(body_content)
                    else:
                        data = parse_string(body_content)
                else:
                    data = parse_string(body_content)
        except Exception as e:   # pragma: no cover
            logging.debug("An error occurred processing the body request:\n------------------------------------------\n%s\n------------------------------------------\n%s\n------------------------------------------\n" % (self.request.body, str(e)))

        files = []

        # python 2-3 compatibility
        try:
            files_iteritems = self.request.files.iteritems()
        except AttributeError:  # pragma: no cover
            files_iteritems = self.request.files.items()

        for file_data in files_iteritems:
            file_data = file_data[1][0]
            files.append({'name': file_data['filename'], 'content': file_data['body']})

        host = self.request.host
        protocol = self.request.protocol
        remote_ip = self.request.remote_ip
        version = self.request.version

        return Request(method, path, query, data, files, headers, host, protocol, remote_ip, version)

    def _serve(self):
        try:
            request = self.get_request()

            response = self.dispatcher.dispatch(request)
            response_content = response.get_content()

            self.set_status(response.get_status_code(), response.get_status_text())

            for header_name, header_value in response.headers.all().items():
                self.add_header(header_name, header_value)

            if not isinstance(response_content, six.string_types):
                raise Exception("The response.get_content() must return a string. %s given." % type(response_content))
        except Exception:
            traceback.print_exc(file=sys.stderr)
            response = self.error_handler.get_internal_server_error_response(request)
            self.set_status(response.get_status_code())
            response_content = response.get_content()
            self.set_status(response.get_status_code())

        self.write(response_content)
        self.finish()


def get_body_content_from_request_body(request_body):
    try:
        # python 3
        body_content = str(request_body, encoding='UTF-8')
    except TypeError:    # pragma: no cover
        # python 2
        body_content = request_body

    return body_content


def parse_string(string=''):
    """Build a params dictionary from a string.

    Duplicate key/value pairs in the provided string will be
    returned as {'key': [val1, val2, ...]}. Single key/values will
    be returned as strings: {'key': 'value'}.
    """

    if not string:
        return {}

    if isinstance(string, bytes):
        string = str(string)

    def unquote_qs(string_):
        # python 2-3 compatibility
        try:
            from urllib import unquote
        except:    # pragma: no cover
            from urllib.parse import unquote

        return unquote(string_.replace('+', ' '))

    pairs = [s2 for s1 in string.split('&') for s2 in s1.split(';')]
    d = {}
    for name_value in pairs:
        nv = name_value.split('=', 1)
        if len(nv) != 2:
            nv.append('')

        name = unquote_qs(nv[0])
        value = unquote_qs(nv[1])

        if name in d:
            if not isinstance(d[name], list):
                d[name] = [d[name]]
            d[name].append(value)
        else:
            d[name] = value
    return d


class ServerAdapter(BaseServerAdapter):
    def __init__(self, settings, dispatcher, error_handler):
        BaseServerAdapter.__init__(self, settings, dispatcher, error_handler)
        self._workers = -1
        if 'workers' in settings and settings['workers'] > 0:
            self._workers = settings['workers']

        MainHandler.dispatcher = self._dispatcher
        MainHandler.error_handler = self._error_handler

        application = Application([
            (r"/.*", MainHandler),
        ])

        self._http_server = HTTPServer(application)

    def run(self):
        self._http_server.bind(self._port)
        self._http_server.start(self._workers)
        IOLoop.instance().start()
