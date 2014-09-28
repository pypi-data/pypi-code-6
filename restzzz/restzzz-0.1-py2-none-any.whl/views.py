""" Cornice services.
"""
import pyramid.exceptions as exc
from cornice import Service
import zmq
from pprint import pprint

from restzzz.zmqwrap import PubSocket, SubSocket

# Storage for the two socket types
_SOCKETS_GET = {}
_SOCKETS_POST = {}
_CFG = {}

# Endpoint for getting the list of available endpoints
socklist = Service(name='socketlist', path='/', description="List sockets")
# Endpoint for getting/sending data
sockserv = Service(name='restzzz', path='/{queue}', description="RESTZZZ app")


@socklist.get()
def get_info(request):
    """ Returns the list of available endpoints. """
    #return {"get": _SOCKETS_GET, "post": _SOCKETS_POST}
    return _CFG

@sockserv.get()
def get_sock(request):
    qname = request.matchdict["queue"]
    if qname in _SOCKETS_GET:
        return _SOCKETS_GET[qname].recv()
    raise exc.NotFound

@sockserv.post()
def post_sock(request):
    qname = request.matchdict["queue"]
    if qname in _SOCKETS_POST:
        return _SOCKETS_POST[qname].send(request.body)
    raise exc.NotFound

def load_sockets(cfg):
    _CFG.update(cfg)
    ctx = zmq.Context.instance()
    for name, settings in cfg.get("get", {}).items():
        _SOCKETS_GET[name] = SubSocket(settings["connect"],
                                       settings.get("subject", ""))
    for name, settings in cfg.get("post", {}).items():
        _SOCKETS_POST[name] = PubSocket(settings["connect"],
                                        settings.get("subject", None))

