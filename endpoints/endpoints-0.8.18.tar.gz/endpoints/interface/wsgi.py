
class WSGI(BaseInterface):
    def handle(self, environ, start_response):
        c = self.get_call_instance(environ)
        res = c.handle()

        start_response(
            '{} {}'.format(res.code, res.status),
            [(k, v) for k, v in res.headers.iteritems()]
        )
        return [res.body]

    def get_request_instance(self, environ, *args, **kwargs):
        r = Request()
        for k, v in environ.iteritems():
            if k.startswith('HTTP_'):
                r.headers[k[5:]] = v

        r.method = environ['REQUEST_METHOD']
        r.path = environ['PATH_INFO']
        r.query = environ['QUERY_STRING']
        r.environ = environ

        if r.is_method('POST'):
            r.body = environ['wsgi.input'].read()

        return r

    def __call__(self, environ, start_response):
        return self.handle(environ, start_response)


from BaseHTTPServer import HTTPServer
import os
import argparse

from .interface import PythonHTTP


def console():
    parser = argparse.ArgumentParser(description='Endpoints -- Simple server')
    parser.add_argument(
        '--dir', '-d',
        dest='dir',
        default=os.curdir,
        help='directory to server from, defaults to current working directory'
    )
    parser.add_argument(
        '--port', '-p',
        dest='port',
        default=8000,
        type=int,
        help='the port for the webserver'
    )
    parser.add_argument(
        '--prefix',
        dest='prefix',
        default='',
        help='the controller prefix'
    )

    args = parser.parse_args()

    if args.prefix:
        os.environ['ENDPOINTS_PREFIX'] = args.prefix

    server_address = ('', args.port)
    httpd = HTTPServer(server_address, PythonHTTP)
    httpd.serve_forever()
    #httpd.handle_request()

