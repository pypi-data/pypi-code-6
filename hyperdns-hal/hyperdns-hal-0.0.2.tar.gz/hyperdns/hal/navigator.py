"""Navigate HAL representations produced by the render module.

This library extends https://github.com/deontologician/rest_navigator
to generate a client side object model that matches the model exposed.
To the extent possible, the object model can be used as if the object
graph represented by the HAL REST API were local.

This also uses jwt for security.

For example:

baseClass=HALRoot(baseUrl)

In addition, behaviour can be associated with server side classes through
an attachment mechanism.

For Example:

@Navigator.attach('myClass')
def aMethod(self):
    pass
    
will allow instances of Navigator corresponding to the 'myClass' class on
the server to have aMethod().
"""
import json
import os
import inspect,logging
from restnavigator import HALNavigator
from types import MethodType

import collections

navlog=None
def logger():
    global navlog
    if navlog==None:
        navlog=logging.getLogger('hal.navigator')
    return navlog
    
class ndict(collections.MutableMapping):
    """Collection to catch setitem and delitem and propagate those changes
    up to the server. 
    """
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.name=args[0]
        self.parent=args[1]
        self.update(dict((), **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        print("Should update on server",key,value)
        print("Coll:%s, Item '%s' updated - should update on server" % (self.name,key))
        self.store[key]=value

    def __delitem__(self, key):
        print("Coll:%s, Item '%s' removed - should delete from server" % (self.name,key))
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)
        
    def init_assign(self,key,value):
        self.store[key]=value
        
class Navigator(object):
    """Wrapper around rest_navigator's HALNavigator
    """
    registry={}

    class attach_class(object):
        """This annotation is used by clients to register methods that should
        be attached to specific types.
        """
        def __init__(self):
            """Ensure that we have a function map for the given target
            in the Navigator's global registry."""
            pass
            
        def _decorate_method(self,f):
            """This returns a unique wrapper around f, avoiding the re-use of the method
            in local storage when this is in the _call loop body
            """
            def decorated(obj,*args, **kwargs):
                try:
                    obj._ensure_populated()
                    result=f(obj,*args, **kwargs)
                    #obj._refresh_from_server()
                    #print("OPERATION %s returned %s" % (f,result))
                except Exception as E:
                    logger().warn("%s:%s raised exception %s" % (self.target,f.__name__,E))
                    raise
                return result
            decorated.__name__=f.__name__
            return decorated
            
        def __call__(self,class_):
            """This will attach all the methods of this class onto the
            loaded vendor classes.
            """
            self.target=class_.__name__
            self.functions=Navigator.registry.setdefault(self.target,{})
            for (name,f) in inspect.getmembers(class_, predicate=inspect.isfunction):
                self.functions[f.__name__]=self._decorate_method(f)
            return class_

    class attach(object):
        """This annotation is used by clients to register methods that should
        be attached to specific types.
        """
        def __init__(self,target):
            """Ensure that we have a function map for the given target
            in the Navigator's global registry."""
            self.functions=Navigator.registry.setdefault(target,{})
            
        def __call__(self,f):
            """We make sure that methods are read from the server before
            any of the attached methods are accessed.  This allows us to
            use lazy loading transparent to method calls.
            """
            def decorated(obj,*args, **kwargs):
                obj._ensure_populated()
                return f(obj,*args, **kwargs)
            d=decorated
            d.__name__=f.__name__
            self.functions[f.__name__]=d
            return d

    class MissingJWT(Exception):
        """Thrown when we can not determine a security token
        """
        def __init__(self,url,jwt=None,parent=None):
            self.url=url
            self.jwt=jwt
            self.parent=parent
            
    def __init__(self,url,raw=None,jwt=None,parent=None,delay=False,nav=None):
        """create a navigator from an optional raw argument, a
        parent or a jwt credential (in the case of a root object).
        """
        self.url=url
        if raw!=None:
            self.url=raw['_links']['self']['href']

        # establish a value for the JWT
        if jwt==None and parent==None:
            raise self.MissingJWT(url)
        self._parent=parent
        if jwt==None:
            jwt=parent._jwt
        self._jwt=jwt
    
        # build the HALNavigator
        if nav==None:
            nav=HALNavigator(
                self.url,apiname=self.__class__.__name__)
            hdrs={}
            hdrs['Authorization']='Bearer %s' % self._jwt
            nav.session.headers.update(hdrs)   
        self._navigator=nav
        
        # these are collections and complex objects
        self._navigables={}
                            
        # if we have a value, either via raw JSON or if we want to load eagerly
        # then update this representation
        self._loaded=False
        if raw==None:
            if not delay:
                self._refresh_from_server()
        else:
            self._copy_from_raw(raw)

    # -----------------------------------------------------------------------
    # Mapping the representation from HAL into native python
    def _process_embedded(self,embeds):
        # now process embedded objects
        for name,elt in embeds.items():
            existing=self._navigables.get(name,None)
            if elt==None:
                self._navigables[name]=None
            else:
                if isinstance(existing,Navigator):
                    existing._copy_from_raw(elt)
                else:
                    impl=self._navigables.get(name,ndict(name,self))
                    keyfield=elt.get('keyfield',None)
                    if keyfield==None:
                        raise Exception('Can not autopopulate, missing keyfield in collection %s' % name)
                    collection_data=elt.get('_embedded',{}).get(name)
                    for halObject in collection_data:
                        idx=halObject.get(keyfield,None)
                        if idx==None:
                            raise Exception('Raw hal data for embedded element of collection %s failes to have index field %s' % (name,keyfield))
                        existing=impl.get(idx)
                        if existing==None:
                            raise Exception('Failed to find item %s in collection %s, should have been created by links' % (idx,name))
                        #print("copying from raw: item %s:%s[%s]" % (halObject['_class_name'],name,idx),halObject)
                        existing._copy_from_raw(halObject)
                    pass
                    

    def _process_links(self,links,curies=None):
        """Apply custom link processing to the links.  Currently this means
        that we look for collections via link relations prefaced by cbase:
        """
        if curies==None:
            curies = {curie['name']: curie['href']
                        for curie in links.get('curies',{})}

        # build a list of scalars based on the _links section
        scalars={
            rel.split(":")[1]:link
                for rel,link in links.items()
                if rel.startswith('sbase:')}
        for s_name,link in scalars.items():
            #print("LINK:",type(link),self.url,link.uri,link.template_uri)
            urx='%s/%s' % (self.url,s_name)
            #print("LINK",link.expand())
            scalar=self._navigables.setdefault(s_name,None)
            if scalar==None:
                self._navigables[s_name]=Navigator(
                        urx,parent=self,delay=True,nav=None)
                    
        # build a list of collections based on the _links section
        collections={
            rel.split(":")[1]:keyarray
                for rel,keyarray in links.items()
                if rel.startswith('cbase:')}

        # create lazy-loading collections
        for c_name,c_keyarray in collections.items():
            found={}
            impl=self._navigables.setdefault(c_name,ndict(c_name,self))
            for key in c_keyarray:    
                # key is a navigator, ready to be loaded
                idx=str(key.title)
                found[idx]=True
                if idx not in impl:
                    impl.init_assign(idx,Navigator(key.uri,parent=self,delay=True,nav=key))

            # now prune any items that failed to show up in the collection
            for idx in list(impl):
                if idx not in found:
                    del impl[idx]

    def _ensure_populated(self):
        """Refresh this object from server, if it has not been loaded"""
        #if self._navigator.response==None:
        #    self._refresh_from_server()
        if not self._loaded:
            self._refresh_from_server()
                   
    def _copy_from_raw(self,raw):
        """Digest the raw JSON and update the local instance."""
        self._navigator._process_raw_json(raw,raise_exc=False)
        self._process_links(dict(self._navigator._links),self._navigator.curies)
        embeds=raw.get('_embedded',{})
        self._process_embedded(embeds)
        self._loaded=True
        
    def _refresh_from_server(self):
        """Update the representation of the navigator.  This calls the
        underlying navigators _GET() method, and then adds the additional
        behaviour to process the _links and the _embedded.
        """
        self._navigator._GET()
        if self._navigator.status[0]!=200:
            raise Exception('Failed to obtain %s, result=%s' %
                 (self._navigator.uri,self._navigator.status))
        self._process_links(self._navigator.links,self._navigator.curies)
        raw=self._navigator.response.json()
        embeds=raw.get('_embedded',{})
        self._process_embedded(embeds)
        self._loaded=True
        return True
        
    # This allows OBJ.<prop> to look up <prop> in the list of possible collections
    # or object references, and then to fetch and populate it if required
    def __getattr__(self,key):
        """Look for and return a property that may be a regular property, a scalar, or
        a collection, fetching the object from the server if required.
        """
        #if self._navigator.response==None:
        #    if not self._refresh_from_server():
        #        raise Exception('Failed to obtain resource from server')
        if not self._loaded:
            if not self._refresh_from_server():
                raise Exception('Failed to obtain resource from server')
               
        # look for primitive properties
        if key in self._navigator.state:
            return self._navigator.state[key]
            
        # look for collections
        if key in self._navigables:
            impl=self._navigables[key]
            return impl
            
        # now look for possible methods    
        cname=self._navigator.state.get('_class_name',None)
        if cname==None:
            raise AttributeError('The navigator has been refreshed with a non-HAL object, corrupt type is %s' % (cname))
        
        if cname in Navigator.registry:
            #print("Looking for %s in method list %s" % (key,Navigator.registry[cname]))
            method=Navigator.registry[cname].get(key)
            if method!=None:
                return MethodType(method,self)
        #else:
        #    raise Exception('Nothing registered for %s' % cname)
        
        #return super(Navigator,self).__getattr__(key)
        raise AttributeError('Can not find %s, in object of type %s' % (key,cname))

    def __getitem__(self,getitem_args):
        return self._navigator.__getitem__(getitem_args)
        
    def __repr__(self):
        if self._navigator.state==None:
            cname="Unfetched"
        else:
            cname=self._navigator.state.get('_class_name','Unknown Navigator')
        return "%s(url=%s,clist=%s)" % (
            cname,self.url,
            json.dumps(list(self._navigables.keys())))


    # -----------------------------------------------------------------------
    # breaking from RESTfulness
    class BadCall(Exception):
        """Thrown when a response is not the expected type.
        """
        def __init__(self,response):
            self.response=response
            
        def __str__(self):
            if self.response.status_code==422:
                return "%s" % self.response.content.decode('utf-8')
            else:
                return "BadCall, http response %s" % self.response.status_code 
            
    def _handle_response(self,response,raw):
        """Process HTTP 200 by decoding UTF-8 or parsing JSON, and raising
        and exception if the response was other than HTTP 200.
        """
        if response.status_code==200:
            if raw:
                return response.content.decode("utf-8")
            else:
                return response.json()
        else:
            raise self.BadCall(response)
        
    def post(self,uri,data={},raw=False,includes_refresh=False):
        """Post to a uri relative to this resource, sending optional data
        and returning either JSON or raw data.
        """
        url="%s%s" % (self.url,uri)
        session=self._navigator.session
        body=json.dumps(data)
        headers={}
        headers['Content-Type']='application/json'
        headers['Content-Length']=len(body)
        response=session.post(url,headers=headers,data=body)
        result=self._handle_response(response,raw)
        if includes_refresh:
            print("REFRESHING:",result)
            self._copy_from_raw(result)
        return result
        
    def get(self,uri,data={},raw=False):
        """Read from a uri relative to this resource, sending optional JSON data
        and returning either JSON or raw data.
        """
        url="%s%s" % (self.url,uri)
        session=self._navigator.session
        body=json.dumps(data)        
        headers={}
        headers['Content-Type']='application/json'
        headers['Content-Length']=len(body)
        response=session.get(url,data=body,headers=headers)
        return self._handle_response(response,raw)

    def delete(self,uri=""):
        """Read from a uri relative to this resource, sending optional JSON data
        and returning either JSON or raw data.
        """
        url="%s%s" % (self.url,uri)
        session=self._navigator.session
        response=session.delete(url)
        return self._handle_response(response,raw=False)
    
#
class HALRoot(Navigator):
    """Create a Navigator which relates a security token and a base URL, and
    which has no parent.  This is the single required HAL endpoint.
    """
    def __init__(self,jwt,baseUrl):
        super(HALRoot,self).__init__(baseUrl,
            jwt=jwt,
            parent=None)
#
