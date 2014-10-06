import json
import pkg_resources


def pkg_resources_version(package):
    try:
        version = pkg_resources.require(package)[0].version
    except IndexError:
        version = 'Error reading version with pkg_resources.require'
    return version


def package_version(package):
    version = pkg_resources_version(package)

    def inner():
        return version
    return inner


class ApplicationVersion(object):

    def __init__(self, application, determine_version=None, version_url='/version'):
        if determine_version is None:
            msg = ('`determine_version` argument is required. It must be '
                   'either a package name or callable that returns the '
                   'package version')
            raise TypeError(msg)
        if not callable(determine_version):
            determine_version = package_version(determine_version)

        self.determine_version_callable = determine_version
        self.application = application
        self.version_url = version_url

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if path == self.version_url:
            response_callable = self.application_version
        else:
            response_callable = self.application
        return response_callable(environ, start_response)

    def application_version(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        if method != 'GET' and method != 'HEAD':
            start_response('405 Method Not Allowed', [('Allow', 'GET, HEAD')])
            return []
        headers = [('Content-Type', 'application/json')]
        start_response('200 OK', headers)
        return [json.dumps({'version': self.determine_version_callable()})]
