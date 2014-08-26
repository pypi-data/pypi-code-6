"""
Fanery wsgi handler.
"""
__all__ = ['build_handler']

from mimetypes import guess_type, add_type
add_type('application/json', '.json')

from webob import Response
from webob.dec import wsgify
from webob.static import FileApp, DirectoryApp
from webob.exc import HTTPBadRequest, HTTPNotFound, HTTPNotImplemented

from _term import (
    Hict, parse_json, to_simple, to_json,
    is_file_path, is_dir_path, is_sequence, is_generator
)
from _service import consume
from _state import State
from _exc import NotFound
from _version import __version__

SERVER = 'Fanery/%s' % __version__
CONTENT_TYPE = 'text/plain'
CHARSET = 'utf8'
ENCODING_ERROR = u"Wrong request encoding, must be %s." % CHARSET
PARSING_ERROR = u"Wrong request parameters format, unable to parse."

from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

import logging
logger = logging.getLogger('fanery.wsgi')


def http_time(stamp=None):
    return format_date_time(stamp or mktime(datetime.now().timetuple()))


@wsgify
def handler(req):
    req.charset = CHARSET

    try:
        argd, params, path = Hict(), req.params, req.path

        for key in params.iterkeys():
            if not key.startswith('_'):
                if key.endswith('[]'):
                    argd[key[:-2]] = params.getall(key)
                else:
                    argd[key] = params[key]

        if '_json_' in params:
            argd.update(parse_json(params['_json_']))

    except UnicodeDecodeError:
        return HTTPBadRequest(ENCODING_ERROR, server=SERVER)
    except:
        return HTTPBadRequest(PARSING_ERROR, server=SERVER)

    _state_ = State(domain=req.host.split(':', 1)[0],
                    origin=req.client_addr or '127.0.0.1',
                    sid=None, profile=None, role=None,
                    ssl=bool(req.headers.get('X-Forwarded-Proto', req.scheme) == 'https'))                  # noqa

    try:
        fun, ext, ret = consume(_state_, path, **argd)
    except NotFound, e:
        return HTTPNotFound(server=SERVER)
    except NotImplementedError, e:
        return HTTPNotImplemented(server=SERVER)
    except Exception, e:
        res = HTTPBadRequest(content_type='text/plain', server=SERVER)
        error = dict(exc=e.__class__.__name__, err=e.args)
        res.body = to_json(to_simple(error))
        return res

    headers = {'X-Frame-Options': 'SAMEORIGIN', 'X-XSS-Protection': '1; mode=block'}                        # noqa

    if fun.ssl:
        headers['Strict-Transport-Security'] = "max-age=31536000; includeSubDomains"                        # noqa

    if fun.static:
        headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' 'unsafe-eval'"             # noqa

        if not fun.cache:
            headers['Cache-Control'] = 'max-age=0, must-revalidate, no-cache, no-store'                     # noqa
            headers['Pragma'] = 'no-cache'
            headers['Expires'] = 0

        if isinstance(ret, file):
            with ret:
                ret = ret.name

        if is_file_path(ret):
            headers['X-Content-Type-Options'] = 'nosniff'

            if fun.force_download:
                # Do NOT use Content-Disposition [RFC-6266 Section 7]
                headers['Content-Type'] = 'application/octet-stream'
            else:
                headers['Content-Type'] = guess_type(ret)[0] or CONTENT_TYPE

            x_accel = fun.accel
            if x_accel:
                headers['X-Accel-Redirect' if x_accel == 'nginx' else 'X-Sendfile'] = ret                   # noqa
                return Response(server=SERVER, headerlist=headers.items())
            else:
                return FileApp(ret, server=SERVER, headerlist=headers.items())

        elif is_dir_path(ret):
            return DirectoryApp(ret, server=SERVER)

        else:
            return HTTPNotFound(server=SERVER)

    else:
        headers['Content-Security-Policy'] = "default-src 'none'"

        res = Response(server=SERVER, charset=CHARSET, headerlist=headers.items(),                          # noqa
                       content_type=guess_type(path)[0] or CONTENT_TYPE)

        if isinstance(ret, str):
            res.body = ret
        elif isinstance(ret, unicode):
            res.unicode_body = ret
        elif is_sequence(ret) or is_generator(ret):
            res.app_iter = ret
        elif isinstance(ret, file):
            res.body_file = ret
        else:
            res.body = repr(ret)

        cache = fun.cache
        if not cache:
            res.cache_expires(0)
        elif isinstance(cache, int):
            res.cache_expires(cache)
        else:
            res.cache_expires(86400)

        return res


def build_handler(wsgi_app=handler, profile=False, **argd):

    if profile is True:
        from linesman import middleware
        open(middleware.ENABLED_FLAG_FILE, 'w').close()
        wsgi_app = middleware.make_linesman_middleware(wsgi_app, **argd)
        logger.info("wsgi profiler path is %s" % wsgi_app.profiler_path)

    return wsgi_app
