import os
#from endpoints.interface.wsgi import Server
import uuid

#os.environ['ENDPOINTS_PREFIX'] = 'mycontroller'
#application = Server()

from collections import deque

#from twisted.web.http_headers import _DictHeaders, Headers

from Cookie import SimpleCookie, Morsel
from ZODB import DB
from ZEO import ClientStorage

import logging
logging.basicConfig()

from ZEO import ClientStorage
from ZODB import DB
import transaction

# Change next line to connect to your ZEO server
addr = '192.168.30.30', 8000
storage = ClientStorage.ClientStorage(addr)
db = DB(storage)
conn = db.open()
zroot = conn.root()

def get_session_id(request):
    cookie = request.HTTP_COOKIE.split(';')
    return cookie.split('session=')[-1]

def get_request_method(request):
    return request.REQUEST_METHOD

def path_elements(request):
    path = request.PATH_INFO[1:]
    l = len(path)
    if l > 0:
        if path[l-1]=='/':
            path = path[:l-1]
    if path.count('/') >= 1:
        return deque(path.split('/'))
    if path == '':
        return deque([])
    return deque([path])

from zope.interface import (
    implements,
    Interface)


class IRequest(Interface):
    pass


class Request(object):
    implements(IRequest)
    def __init__(self, request):
        for key in request.keys():
            val = request[key]
            self[key] = val
        self.prepath = []
        self.postpath = []

    def __setitem__(self, key, val):
        setattr(self, key, val)


    def __getitem__(self, key):
        return getattr(self, key)

    def keys(self):
        return self.__dict__.keys()

    def __repr__(self):
        return str(self.__dict__)


def path_to_Resource(path):
    path = path[1:]
    current = root
    for entry in path:
        current = current._mappings[entry]
    return current


class Resource(object):
    def __init__(self, name=None):
        self._mappings = {}
        self.name = 'root'
        self.path = list()
        self.parent = ""

    def render_POST(self, request):
        pass

    def print_name(self):
        print "My name is %s" % self.name

    def render_GET(self, request):
        return "My name is %s. My parent is %s. My path is %s" % (self.name, self.parent, self.path)

    def putChild(self, name, resource, force=False):
        if (not name in self._mappings) or force:
            self._mappings[name] = resource
            resource.name = name
            resource.parent = self.name
            resource.path = self.path
            resource.path.append(self.name)

    def getChild(self, name, request):
        print "### GET CHILD CALLED %s"%(name)
        if name in self._mappings.keys():
            return self._mappings[name](request)

    def __call__(self, request):
        len_postpath = len(request.postpath)
        if len_postpath >= 1:
            name = request.postpath.popleft()
            request.prepath.append(name)
            return self.getChild(name, request)
        if len_postpath == 0:
            method = str(get_request_method(request)).upper()
            return getattr(self, 'render_%s'%(method))(request)

#### TREE ####################################################################

class Root(Resource):

    def render_GET(self, request):
        return "THIS IS ROOT"

class Owned(Resource):

    def findPrinciple(self):
        self.principle = self.path[1]
        return self.principle

class OneHandler(Resource):

    def render_GET(self, request):

        return "ONE HANDLER. My parent is %s" %self.parent

class TwoHandler(Resource):
    pass

class ThreeHandler(Resource):

    def render_GET(self, request):
        if zroot.keys() == []:
            for x in range(0, 100):
                name = "hello%s"%(str(x))
                zroot[name] = Root()
            transaction.commit()
        return str(zroot.keys())

root = Root()
one =  OneHandler()
two = TwoHandler()
three = ThreeHandler()

root.putChild('1', one)
one.putChild('2', two)
two.putChild('3', three)


def persist_session(request):
    print "#################"
    print request['HTTP_COOKIE']
    print "#################"

def get_session_id():
    return str(uuid.uuid4())

def set_cookie_session(headers, session_id):
    session_cookie = SimpleCookie()
    session_cookie['session'] = session_id
    session_cookie['session']["Path"] = '/'
    cookieheaders = ('Set-Cookie', session_cookie['session'].OutputString())
    headers.insert(0, cookieheaders)
    return headers

def get_request(env):
    if not IRequest.providedBy(env):
        request = Request(env)
        request.postpath = path_elements(request)
    return request

def application(env, start_response):
    request = get_request(env)
    headers = [('content-type', 'text/html')]
    if not 'HTTP_COOKIE' in request.keys():
        request['HTTP_COOKIE'] = session_id = get_session_id()
        headers = set_cookie_session(headers, session_id)
        persist_session(session_id)
    result = root(request)
    start_response('200 OK', headers)
    return [result]
    #return ["HELLO WORLD"]