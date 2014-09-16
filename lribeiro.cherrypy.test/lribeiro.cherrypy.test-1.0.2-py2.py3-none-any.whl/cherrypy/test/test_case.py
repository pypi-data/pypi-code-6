"""
CPTestCase.request method borrowed from https://bitbucket.org/Lawouach/cherrypy-recipes/src/
"""

import re
from io import BytesIO

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import unittest

import cherrypy

from . import httpstatus

METHODS_WITH_BODY = ('POST', 'PUT')
REDIRECT_STATUS = (httpstatus.MOVED_PERMANENTLY, httpstatus.FOUND, httpstatus.SEE_OTHER)


# Not strictly speaking mandatory but just makes sense
cherrypy.config.update({'environment': "test_suite"})

# This is mandatory so that the HTTP server isn't started
# if you need to actually start (why would you?), simply
# subscribe it back.
cherrypy.server.unsubscribe()

# do not output any log to the console
cherrypy.log.screen = False

# simulate fake socket address... they are irrelevant in our context
_fake_local_host = cherrypy.lib.httputil.Host('127.0.0.1', 50000, "")
_fake_remote_host = cherrypy.lib.httputil.Host('127.0.0.1', 50001, "")


class CPTestCase(unittest.TestCase):

    _script_name = '/'
    preserve_cookies = True
    "Whether to preserve cookies between requests"

    def __init__(self, *args, **kwargs):
        super(CPTestCase, self).__init__(*args, **kwargs)
        self.current_request = None
        self.current_response = None
        self.cookies = None

    @classmethod
    def setUpClass(cls):
        script_name = getattr(cls, 'script_name', cls._script_name)
        config = getattr(cls, 'config', {})
        root = cls.root

        cherrypy.tree.mount(root, script_name, config)
        cherrypy.engine.start()

    @classmethod
    def tearDownClass(cls):
        cherrypy.engine.exit()

    def request(self, path='/', method='GET', app_path='', scheme='http', proto='HTTP/1.1',
                data=None, headers=None, cookies=None, auto_redirect=False, **kwargs):
        # if path is absolute, remove server part
        if path.startswith(cherrypy.url('/')[:-1]):
            path = path[len(cherrypy.url('/')[:-1]):]

        # if path is absolute but for an external domain, just return the domain and clear the current request/response
        if re.match('^https?://', path) is not None:
            self.current_request = None
            self.current_response = None
            return path

        # Ensure path starts with '/'
        if not path.startswith('/'):
            path = '/' + path

        # This is a required header when running HTTP/1.1
        h = {'Host': '127.0.0.1'}

        if headers is not None:
            h.update(headers)

        # If we have a POST/PUT request but no data
        # we urlencode the named arguments in **kwargs
        # and set the content-type header
        if method in METHODS_WITH_BODY:
            h['content-type'] = 'application/x-www-form-urlencoded'

            if not data:
                data = kwargs
                kwargs = None

            data = urlencode(data).encode('utf-8')

        # If we did have named arguments, let's
        # urlencode them and use them as a querystring
        qs = None
        if kwargs:
            qs = urlencode(kwargs)

        # if we had some data passed as the request entity
        # let's make sure we have the content-length set
        fd = None
        if data is not None:
            h['content-length'] = '%d' % len(data)
            fd = BytesIO(data)

        # Get our application and run the request against it
        app = cherrypy.tree.apps.get(app_path)
        if not app:
            raise Exception("No application mounted at '%s'" % app_path)

        # Cleanup any previous returned response
        # between calls to this method
        app.release_serving()

        # Let's fake the local and remote addresses
        request, response = app.get_serving(_fake_local_host, _fake_remote_host, scheme, proto)

        # Set up cookies
        # It needs to be in the headers because cherrypy assigns a new SimpleCookie inside Request.run() method
        if cookies:
            h['Cookie'] = urlencode(cookies)
            if self.preserve_cookies:
                self.cookies = cookies
        elif self.cookies:
            set_cookie = 'Set-Cookie: '
            h['Cookie'] = self.cookies.output().lstrip(set_cookie)

        try:
            h = [(k, v) for k, v in h.items()]
            response = request.run(method, path, qs, proto, h, fd)
        finally:
            if fd:
                fd.close()
                fd = None

        # store the cookies for next requests
        if self.preserve_cookies and len(response.cookie) > 0:
            if self.cookies is None:
                self.cookies = response.cookie
            else:
                self.cookies.update(response.cookie)

        if auto_redirect and 'Location' in response.headers:
            location = response.headers['Location']
            return self.request(location)

        # collapse the response into a bytestring
        body = response.collapse_body()

        # set more usable values on the response object
        response.text = bytes.decode(body, 'utf-8')
        response.status_code = int(response.status.split(' ')[0])

        self.current_request = request
        self.current_response = response

        return response

    # Methods to get responses
    def get(self, path, **kwargs):
        return self.request(path, method='GET', **kwargs)

    def post(self, path, **kwargs):
        return self.request(path, method='POST', **kwargs)

    def put(self, path, **kwargs):
        return self.request(path, method='PUT', **kwargs)

    def delete(self, path, **kwargs):
        return self.request(path, method='DELETE', **kwargs)

    def head(self, path, **kwargs):
        return self.request(path, method='HEAD', **kwargs)

    def patch(self, path, **kwargs):
        return self.request(path, method='PATCH', **kwargs)

    # Assertions
    def assert_status(self, status_code, msg=None):
        self.assertEqual(status_code, self.current_response.status_code, msg)

    def assert_ok(self, msg=None):
        self.assert_status(httpstatus.OK, msg)

    def assert_not_found(self, msg=None):
        self.assert_status(httpstatus.NOT_FOUND, msg)

    def assert_error(self, msg=None):
        self.assert_status(httpstatus.INTERNAL_SERVER_ERROR, msg)

    def assert_redirect(self, msg=None):
        self.assertTrue(self.current_response.status_code in REDIRECT_STATUS, msg)

    def assert_redirect_to(self, to, msg=None):
        status_code_correct = self.current_response.status_code in REDIRECT_STATUS
        header_correct = self.current_response.headers['Location'] == cherrypy.url(to)
        self.assertTrue(status_code_correct and header_correct, msg)

    def assert_not_redirect(self, msg=None):
        self.assertNotIn(self.current_response.status_code, REDIRECT_STATUS, msg)

    def assert_contains(self, text, msg=None):
        self.assertIn(text, self.current_response.text, msg)

    def assert_not_contains(self, text, msg=None):
        self.assertNotIn(text, self.current_response.text, msg)

    def assert_body(self, text, msg=None):
        self.assertEqual(text, self.current_response.text, msg)

    def assert_header(self, header, value, msg=None):
        self.assertIn(header, self.current_response.headers)
        self.assertEqual(value, self.current_response.headers[header], msg)

    def assert_has_header(self, header, msg=None):
        self.assertIn(header, self.current_response.headers, msg)

    def assert_cookie(self, cookie, value, msg=None):
        self.assertIn(cookie, self.current_response.cookie)
        self.assertEqual(value, self.current_response.cookie[cookie].value, msg)

    def assert_has_cookie(self, cookie, msg=None):
        self.assertIn(cookie, self.current_response.cookie, msg)

    def assert_path(self, path, msg=None):
        self.assertEqual(path, self.current_request.path_info, msg)