"""
Third party WSGI Server setup helper function.

Mostly usefull during development and testing.
"""
__all__ = ['start_wsgi_server']

from _wsgi import build_handler

import logging
logger = logging.getLogger('fanery.server')


def start_wsgi_server(wsgi_app=None, host='127.0.0.1', port=9000, ssl=False,
                      bjoern=True, gevent=False, cherrypy=False, **argd):

    if wsgi_app is None:
        wsgi_app = build_handler(**argd)

    logger.info("serving on %s://%s:%s" % ('https' if ssl else 'http', host, port))     # noqa

    if ssl is True:
        from werkzeug.serving import run_simple

        params = dict(ssl_context=argd.get('ssl_context', 'adhoc'),
                      use_reloader=argd.get('use_reloader', True),
                      use_debugger=argd.get('use_debugger', True),
                      use_evalex=argd.get('use_evalex', True),
                      threaded=argd.get('threaded', True))

        try:
            run_simple(host, port, wsgi_app, **params)
        except KeyboardInterrupt:
            pass

    elif cherrypy is True:
        import cherrypy

        cherrypy.tree.graft(wsgi_app, '/')

        cherrypy.config.update({
            'engine.autoreload.on': True,
            'log.screen': True,
            'server.socket_port': port,
            'server.socket_host': host
        })

        try:
            cherrypy.engine.start()
            cherrypy.engine.block()
        except KeyboardInterrupt:
            cherrypy.engine.stop()

    elif gevent is True:
        from gevent.wsgi import WSGIServer

        try:
            WSGIServer((host, port), wsgi_app).serve_forever()
        except KeyboardInterrupt:
            pass

    elif bjoern is True:
        import bjoern

        try:
            bjoern.run(wsgi_app, host, port)
        except KeyboardInterrupt:
            pass

    else:
        from wsgiref.simple_server import make_server

        try:
            make_server(host, port, wsgi_app).serve_forever()
        except KeyboardInterrupt:
            pass
