import sys

from twisted.application import service, internet
from twisted.web import server
from twisted.web import resource
from twisted.internet import defer
from twisted.web.server import NOT_DONE_YET
from twisted.internet import reactor
from twisted.python import log

from routes import Mapper

class TxFlask(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)
        self.map = Mapper()

    def getChild(self, name, req):
        return self

    def render(self, req):
        env = {'REQUEST_METHOD': req.method, 'PATH_INFO': req.path}
        match = self.map.match(environ=env)
        if match is None or match.get('handler', None) is None:
            return resource.NoResource().render(req)
        handler = match.pop('handler')
        result = handler(req, *match.values())
        if isinstance(result, defer.Deferred):
            result.addCallback(self._render, req)
        else:
            self._render(result, req)
        return NOT_DONE_YET

    def _render(self, result, req):
        if not req.finished:
            req.write(result.encode('utf8'))
            req.finish()

    def route(self, path, methods=['GET']):
        def wrapper(func):
            conditions = {'method': methods}
            handler = self.wrap(func)
            self.map.connect(None, path, handler=handler, conditions=conditions)
            return handler
        return wrapper

    def wrap(self, func):
        def runner(req, *args, **kwargs):
            return func(req, *args, **kwargs)
        return runner

    def run(self, port=5000):
        log.startLogging(sys.stdout)
        reactor.listenTCP(port, server.Site(self))
        reactor.run()
