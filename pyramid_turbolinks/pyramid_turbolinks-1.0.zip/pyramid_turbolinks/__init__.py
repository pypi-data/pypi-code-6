from __future__ import unicode_literals

__major__ = 1
__minor__ = 0
__revision__ = 0

__version_info__ = (__major__, __minor__, __revision__)
__version__ = '%s.%s' % (__major__, __minor__)

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

# needed for build system
try:
    from pyramid.events import NewRequest, NewResponse
    from pyramid.httpexceptions import HTTPForbidden
except ImportError:
    pass

def same_origin(current_uri, redirect_uri):
    a = urlparse(current_uri)
    if not a.scheme:
        return True
    b = urlparse(redirect_uri)
    return (a.scheme, a.hostname, a.port) == (b.scheme, b.hostname, b.port)


def process_request(event):
    request = event.request
    referrer = request.environ.get('HTTP_X_XHR_REFERER')
    if referrer:
        # overwrite referrer
        request.environ['HTTP_REFERER'] = referrer
    return


def process_response(event):
    request = event.request
    response = event.response
    referrer = request.headers.get('X-XHR-Referer')
    if not referrer:
        # turbolinks not enabled
        return response

    method = request.cookies.get('request_method')
    if not method or method != request.method:
        response.set_cookie('request_method', request.method)

    if response.location:
        # this is a redirect response
        request.session['_turbolinks_redirect_to'] = response.location

        # cross domain blocker
        if referrer and not same_origin(response.location, referrer):
            return HTTPForbidden()
    else:
        if request.session.get('_turbolinks_redirect_to'):
            loc = request.session.pop('_turbolinks_redirect_to')
            response['X-XHR-Redirected-To'] = loc

    return response


def includeme(config):
    config.add_subscriber(process_request, NewRequest)
    config.add_subscriber(process_response, NewResponse)
    config.add_static_view('turbolinks', 'pyramid_turbolinks:static')