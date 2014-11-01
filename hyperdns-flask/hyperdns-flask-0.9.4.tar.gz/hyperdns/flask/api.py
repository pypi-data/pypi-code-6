"""HAL API annotations for Flask-SQLAlchemy (python3 only).

Basic Usage
    @web.api()
    class myClass(apath_processor.db.Model):
    
        an_index=apath_processor.db.Column(Integer,primary_key)
        sub_object=apath_processor.db.Scalar('myClass')
        a_collection=apath_processor.db.Map('myClass','an_index')

See README.md for more extensive documentation
"""
import sys
import json
import inspect
import traceback
import hyperdns.hal.render as HAL
import hyperdns.flask
from .result import result
from functools import wraps
from flask import request,Response
from  sqlalchemy.orm.attributes import (
    InstrumentedAttribute,
    CollectionAttributeImpl,
    ScalarAttributeImpl
    )
from sqlalchemy.orm.relationships import RelationshipProperty
from urllib.parse import urlparse
from hyperdns.flask import InputExpected,hyperdns_context
from .sql import db_commit


#
class definition(object):
    """Definition objects are created by the @web.api annotation - which will
    produce either definition or api_root objects depending upon whether or
    not the definition is a root or not.  api_roots are subclasses of definitions.
    
    definitions contain the specification of the class - which is the dictionary
    handed in via @web.api({})
    
    the definition class maintains a registry of all defined classes.
    
    the definition is named with the name of the class.
    
    the definition maintains a dictionary of documentation entry points, organized by
    method and 'pseudo-method' - this part is not worked out, and requires the completion
    of the documentaiton browser so that we know what we want here.
    
    the a
    """
    registry={}
    
    def __init__(self,spec,class_):
        
        # record the 
        self.spec=spec

        # save our name, class, and check to make sure we've only been configured once
        # and then store us in the registry under our class name
        self.name=class_.__name__
        self.class_=class_
        assert self.registry.get(self.name)==None
        self.registry[self.name]=self

        self.docs=self.spec.setdefault('docs',{})
        self.docs.setdefault('read','Return a %s' % (self.name))
        
        # it is nearly impossible to pull the attribute documentation out of a sqlalchemy
        # model.  there is a PEP that indicates that the docstring immediately following
        # an attribute definition on a class is the
        self.attrdocs=self.docs.setdefault('attrs',{})
        
    def get_object_definition_docs(self):
        
        docs={
            'doc':self.class_.__doc__,
            'name':self.class_.__name__,
            'properties':{},
            'scalars':{},
            'collections':{}
        }
        
        pset={}        
        for p in self.properties:
            name=p[0]
            doc=self.attrdocs.get(name,None)
            if doc!=None:
                docs['properties'][name]=doc
        for p in self.scalars:
            name=p[0]
            doc=self.attrdocs.get(name,None)
            if doc!=None:
                docs['scalars'][name]={
                    'local':doc,
                    'type':p[1].get_object_definition_docs()
                    }
                
        for (name,defn,key) in self.collections:
            docs['collections'][name]={
                'name':name,
                'key':key,
                'typename':defn.class_.__name__,
                'type':defn.get_object_definition_docs()
            }

        return docs
        
    def get_read_docs(self):
        docs={
            'method':'GET',
            'intro':self.docs['read'],
            'defn':self.get_object_definition_docs(),
            'notes':[{
                'title':"Query Arguments",
                'text':"""
When ?details=True is set, any collections will be returned as
HAL _embedded resources, but if this query parameter is absent
then only the properties and scalars will be returned.
"""
                }
            ]
        }
        return docs

    def __repr__(self):
        return "Defn:%s" % (self.name)
            
#
class api_root(definition):
    """A definition with the 'root' qualifier
    """
    roots={}
    
    def __init__(self,spec,class_):
        super(api_root,self).__init__(spec,class_)
        rootspec=self.spec.get('root')
        assert rootspec!=None
        (self.root_name,self.root_path)=rootspec
        self.roots[self.name]=self
 
    def __repr__(self):
        return "Root:%s" % (self.name)


class context(dict):
    """Method signatures for handler methods receive this augmented dict
    as 
    """
    def __init__(self,kwargs,cursor,path,request):
        self.update(hyperdns_context)
        self.user=hyperdns_context['user']
        self.account=hyperdns_context['account']
        self.object=cursor
        self.obj_path=path
        self.method=request.method
        
        # these will include any arguments in the URI /an/<int:arg>
        self.args=kwargs
        
        # this may be none... see getattr for special processing
        self._input=request.json
        
    @property
    def hasinput(self):
        return self._input!=None
        
    def __getattr__(self,key):
        """If input is requested, but none was provided, throw
        a 'bad-request' error
        """
        if key=='input':
            if self._input==None:
                raise InputExpected()
            return self._input
        raise AttributeError('Unknown attribute %s' % key)
                
                
#
class path_processor(object):
    """path processors are responsible for establishing the object context
    due to the flask path.
    """
    def __init__(self,uri,path,depth=0):
        """record this path relative to a root
        """
        self.root_name=path[:1][0]
        self.uri=uri
        self.depth=depth
        self.object_path=path[1:]
    
    def __repr__(self):
        newpath=self.object_path[:]
        newpath.insert(0,self.root_name)
        return "PP(%d,%s,%s)" % (self.depth,newpath,self.uri)
        
    def for_action(self,arg):
        newpath=self.object_path[:]
        newpath.insert(0,self.root_name)
        uri='%s%s' % (self.uri,arg)
        return path_processor(uri,newpath,self.depth)
        
    def for_child(self,arg):
        newpath=self.object_path[:]
        newpath.insert(0,self.root_name)
        newpath.append(arg)
        uri='%s/%s' % (self.uri,arg)
        return path_processor(uri,newpath,self.depth+1)

    def for_collection(self,c_name,c_index):
        # note the arguments must be unique:
        newpath=self.object_path[:]
        newpath.insert(0,self.root_name)
        newpath.append(c_name)
        #uri='%s/%s/<string:arg_%d>' % (self.uri,c_name,self.depth+1)
        uri='%s/%s/<string:arg_%d_aka_%s>' % (self.uri,c_name,self.depth+1,c_index)
        return path_processor(uri,newpath,self.depth+1)
            
    def setup_context(self,kwargs,request):
        """ set request.hyperdns['context']=web path

        example Path
            ['account','zones','resources']
        is equivalent to
            request.account.zones.get('my.zone.').resources.get('name1')
            
        request.hyperdns['context'] will be the path
        request.hyperdns['parent_context'] will be the last resolved object
            prior to this one, so if the context object is None, then
            you can get to the parent_context and use that to switch.
        """
        
        # arguments are of the form arg_N_aka_name, so we want to strip away
        # the _aka_name part - this gives us the arguments in order, as in
        # arg_0, arg_1, arg_2...
        path_arguments={}
        for arg in kwargs.keys():
            index=arg.find('_aka_')
            if index>=0:
                key=arg[:index]
                path_arguments[key]=kwargs[arg]
                
        # now, get ahold of the root for this request
        root_obj=hyperdns_context.get('available_roots',{}).get(self.root_name)
        
        # and now begin iterating
        cursor=root_obj
        parent_obj=None
        collection=None
        path=[]
        key=None
        scalar_name=None
        collection_name=None
        
        #print("Looking for",self.object_path)
        for path_elt in self.object_path:
            path.append(cursor)

            collection=getattr(cursor,path_elt,None)

            keyname='arg_%s' % (len(path))
            if keyname in path_arguments:
                key=path_arguments[keyname]
                parent_obj=cursor
                #print("deref",key,"in",collection)
                if collection==None:
                    return None
                    
                # @ TODO
                # This breaks if the collection class is indexed, for example, by
                # integers, since the key will be a string
                cursor=collection.get(key)
                collection_name=path_elt
            else:
                parent_obj=cursor
                cursor=collection
                collection=None
                scalar_name=path_elt
                    
        hyperdns_context['context']=cursor
        hyperdns_context['last_key']=key
        hyperdns_context['collection']=collection
        hyperdns_context['collection_name']=collection_name
        hyperdns_context['scalar_name']=scalar_name
        hyperdns_context['parent_obj']=parent_obj
        hyperdns_context['obj_path']=path
        hyperdns_context['root_obj']=root_obj
        hyperdns_context['root_scope']=self.root_name
        return context(kwargs,cursor,path,request)
        
#
class api(object):
    """Indicate that a class is to be exposed, optionally determine
       if it has a root.    
    """
    #             
    def __init__(self,spec={}):
        self.spec=spec
    
    def __call__(self,cls):
        """This populates the registry with unresolved routes
        """        
        if self.spec.get('root')!=None:
            d=api_root(self.spec,cls)
        else:
            d=definition(self.spec,cls)
        return cls

    class action(object):
        """This exposes a POST action on an object.  The object will be located
        and the method called with the JSON data from the request passed as the
        second argument.
    
        Example:
            @web.api()
            class MyModelClass()
            @web.action('/something')
            def a_method(self,context)
    
        """
        def __init__(self,uri,method='POST',hal=False):
            self.uri=uri
            self.method=method
            self.hal=hal
    
        def __call__(self,f):
            f.action={
                'func':f,
                'doc':f.__doc__,
                'uri':self.uri,
                'returns-hal':self.hal,
                'method':self.method
            }
            return f

    @classmethod
    def analyze_route_map(cls,app):
        """Collect all the routes into a dict, organized by URI, then by
        method, with the docstrings attached to each method.
    
        We'll probably collect more info in this, like argument structures
        and such for help with auto-docing, but this is enough for now.
        """
        routes = {}
        for rule in app.url_map.iter_rules():
            info=routes.setdefault(rule.rule,{
                'methods':{}
                })
            mlist=[m for m in rule.methods if m not in ['HEAD','OPTIONS']]
            for m in mlist:
                # grab the doc string from the endpoint that is registered against the class,
                # if it is missing, reply with a "No documentation" message - otherwise, if
                # the doc string starts with a '{' then assume that it is actually a JSON
                # string, so deparse it and hand the object back (otherwise it will be passed
                # to the client as a string) - but if it appears to be a string, then just
                # pass that along unaltered
                d=app.view_functions[rule.endpoint].__doc__
                if d==None:
                    #print("Documentation missing:",rule)
                    d="No documentation available"
                if d[:1]=='{':
                    #print("DOC:",d)
                    info['methods'][m]=json.loads(d)
                else:
                    info['methods'][m]=d
 
        return routes
        
    @classmethod
    def _analyze_model(api):
        """Look through all the classes that have been registered and, for each
            class, determine the properties, scalars, and maps.  Add those to the
            definition associated with that class.  This method does not look
            at the connection between classes, just the construction of each
            class.
        """
        for defn_key in sorted(definition.registry.keys()):
            defn=definition.registry[defn_key]
            spec=defn.spec
            cls=defn.class_
            boring = dir(type('dummy', (object,), {}))
            attrs=[item
                    for item in inspect.getmembers(cls)
                    if item[0] not in boring
                    and not item[0].startswith('_')
                    and isinstance(item[1],InstrumentedAttribute) ]
            defn.properties=[item
                    for item in attrs
                    if isinstance(item[1].impl,ScalarAttributeImpl)
                    and not isinstance(item[1].property,RelationshipProperty)]
            _scalars=[(item[0],
                    definition.registry.get(
                        getattr(item[1].property,'impl_type',None)))
                    for item in attrs
                    if isinstance(item[1].impl,ScalarAttributeImpl)
                    and isinstance(item[1].property,RelationshipProperty)]

            defn.scalars=[(s[0],s[1]) for s in _scalars if s[1] is not None]
            defn.collections=[(item[1].property.key,
                    definition.registry.get(
                        getattr(item[1].property,'impl_type',None)),
                    getattr(item[1].property,'impl_index',None))
                    for item in attrs
                    if isinstance(item[1].impl,CollectionAttributeImpl)]
            
            defn.actions=[item.action
                    for n,item in inspect.getmembers(cls,inspect.isfunction)
                    if hasattr(item,'action') ]
            
            defn.create=None
            if hasattr(cls,'create'):
                defn.create=getattr(cls,'create')
        
            defn.delete=None
            if hasattr(cls,'delete'):
                defn.delete=getattr(cls,'delete')

            defn.update=None
            if hasattr(cls,'update'):
                defn.update=getattr(cls,'update')
        
            
    @classmethod
    def _map_graph(api,defn,path_processor):
        """travel the graph from this element down until we either stop or locate
        a cycle.  each visit occurs within the scope of a root element, forming
        multiple trees as we flatten the graph out.
        """
        # support 'GET'
        api._instrument_read_method(defn,path_processor)
        # support 'POST'
        if defn.create!=None or defn.update!=None:
            api._instrument_write_or_create_method(defn,path_processor)
        # support 'DELETE'
        if defn.delete!=None:
            api._instrument_delete_method(defn,path_processor)
            
        # implement actions
        for action in defn.actions:
            api._instrument_action(defn,path_processor,action)
                
        for (c_name,c_defn,c_index) in defn.collections:
            api._instrument_collection(defn,path_processor.for_child(c_name),c_name,c_index)            
            api._map_graph(c_defn,path_processor.for_collection(c_name,c_index))

        for (s_name,s_defn) in defn.scalars:
            api._map_graph(s_defn,path_processor.for_child(s_name))
            
    @classmethod
    def instrument(api,baseUri=None):
        """Determine what needs to be exposed and then expose it.
        """
        api._analyze_model()

        # now, scan the graph from each root, doing a depth first traversal and
        # setting up an empty array of all the different base uris for each root
        for root in api_root.roots.values():
            uri="%s%s" % (baseUri,root.root_path)
            api._map_graph(root,path_processor(uri,[root.root_name]))
                
        # add HAL support
        for defn in definition.registry.values():
            HAL.attach_HAL_support(
                defn.class_,
                resources=[p[0] for p in defn.scalars],
                collections=[(p[0],p[2]) for p in defn.collections],
                properties=[p[0] for p in defn.properties]
                )
                
        return


    @classmethod
    def _create_read_collection_docs(api,defn,c_name):
        """Generate the displayable read documentation for the
        collection identified by defn
        
        """
        subtype=None
        for (name,c_defn,key) in defn.collections:
            if name==c_name:
                subtype=c_defn
        return "Returns collection of %s object from the %s collection." %\
            (subtype.name,c_name)

    @classmethod
    def _instrument_collection(api,defn,path_processor,c_name,c_index):
        """This attaches the GET method to whole collections.  For example, if your
        model has /my/myMap/<index> as a route, then this is where "reading the
        whole collection" is implemented.
        
        :param defn: the definition object which describes the resource that
                     is represented by this
        :param path_processor: this is the path processor attached to this route
        
        """
        def read_collection(context):
            obj=context.object
            if obj==None:
                return result.not_found()
            return HAL.hal_collection(
                data=obj.values(),name=c_name,keyfield=c_index
                )
        read_collection.__doc__=api._create_read_collection_docs(defn,c_name)
        api._attach_method(defn,path_processor,'GET',read_collection)

    @classmethod
    def _instrument_action(api,defn,path_processor,action):
        """This breaks from the standard HAL/REST model by allowing us the ability
        to respond to arbitrary HTTP requests.
        
        The defn object contains the definition of the class upon which this
        action is defined, and the path_processor contains the information for
        locating this resource from an available root.
        
        The action definition is build up in @web.api.action and is a dictionary
        of data - see that annotation for more documentation.
        
        :param defn: the definition object which describes the resource that
                     is represented by this
        :param path_processor: this is the path processor attached to this route
        """
        def execute_action(context):
            method=action['func']
            if context.object==None:
                return result.not_found()
            return method(context.object,context)
        
        httpMethod=action['method']
        uri=action['uri']
        execute_action.__doc__=action['doc']
        
        # now attach the handler method
        api._attach_method(defn,path_processor.for_action(uri),
                            httpMethod,execute_action)
        
        
    @classmethod
    def _instrument_read_method(api,defn,path_processor):
        """Attach a GET method that will return the object looked up by the
        path processor and defined by :param:defn.
        
        :param defn: the definition object which describes the resource that
                     is represented by this
        :param path_processor: this is the path processor attached to this route
        
        """
        # respond to specific object GETs
        def read_object(context):
            if context.object==None:
                return result.not_found()
            return context.object
                
        # now prepare the documentation
        read_object.__doc__=json.dumps(defn.get_read_docs())
        
        # now attach the method
        api._attach_method(defn,path_processor,'GET',read_object)

    @classmethod
    def _instrument_write_or_create_method(api,defn,path_processor):
        """This attaches a POST handler to either Update or Create a resource.
        The dual use of POST makes things tricky, and probably we should review
        the actual best practices around POST, PUT, and PATCH - I *always* forget
        them.
        
        The function that is called is specified in the definition, the path
        through the object graph, from the root to this resource, is recorded
        in the path processor.
        
        If the context object is None, then this is a create, unless the
        definition does not have a create method.  If the definition fails
        to have a create method and you POST to a resource that does not exist
        we call that a 'forbidden' operation (see result.py)
        
        Likewise, if you POST to an existing resource, and that resource has no
        update method registered, then we call that a forbidden().
        
        :param defn: the definition object which describes the resource that
                     is represented by this
        :param path_processor: this is the path processor attached to this route
        
        """
        # respond to POSTs to create or update objects
        def update_or_create_object(context):
            obj=context.object
            if obj==None:
                if defn.create==None:
                    return result.forbidden()
                obj=defn.create(context)
            else:
                if defn.update==None:
                    return result.forbidden()
                obj=defn.update(obj,context)
            return obj
            
        # now prepare the documentation.
        create_doc="Create is not supported"
        if defn.create!=None:
            create_doc=defn.create.__doc__

        update_doc="Update is not supported"
        if defn.update!=None:
            update_doc=defn.update.__doc__
            
        doc={
            'method':'POST',
            'create':create_doc,
            'update':update_doc
        }
        update_or_create_object.__doc__=json.dumps(doc)
        
        # now attach the actual method handler
        api._attach_method(defn,path_processor,'POST',update_or_create_object)

    @classmethod
    def _instrument_delete_method(api,defn,path_processor):
        """This will attach a handler to the DELETE method.
        
        The function that is called is specified in the definition, the path
        through the object graph, from the root to this resource, is recorded
        in the path processor.
        
        :param defn: the definition object which describes the resource that
                     is represented by this
        :param path_processor: this is the path processor attached to this route
                    - see documentation on path processor class for more information
        """
        # respond to specific object DELETEs
        def delete_object(context):
            obj=context.object
            if obj==None:
                return result.not_found()
            defn.delete(obj,context)
            return result.ok()
            
        # attach the documentation string from the handler function to this
        doc={
            'method':'DELETE',
            'docs':defn.delete.__doc__
        }
        delete_object.__doc__=json.dumps(doc)
        
        # now attach the delete_object method above, to the path processor
        api._attach_method(defn,path_processor,'DELETE',delete_object)
        
            
            
    @classmethod
    def _attach_method(api,defn,path_processor,httpMethod,func):
        """This attaches a method to a route.  This is where we connect a route
        to 
        
        :param defn: the definition object which describes the resource that
                     is represented by this
        :param path_processor: this is the path processor attached to this route
                     - see documentation on path processor class for more information
        :param httpMethod: this is the HTTP METHOD to which to respond
        :param func: the function to call if all of the wrapath_processorers, such as manage
            authentication pass.  func actually implements the business logic part
        :param returns: whether to return 'hal' or 'json'
        
        Note: I don't think we use 'return json' anymore.  we can probably remove it.
        """
        urlparts = urlparse(path_processor.uri)
        urlparts_list = list(urlparts)
        uri=urlparts_list[2]
        
        # this is what binds the existing environment onto the context.
        # this is where the dispatch thread enters the picture - e.g. this is what the
        # Flask system calls when it identifies a registered route.
        # this gets assigned to the target class for the identified resource as an
        # instance method, and it is called on the instance of context or last_context
        def process_object(*args,**kwargs):
            ctx=path_processor.setup_context(kwargs,request)
            
            # if we can not locate a context for this request, issue a generic 404
            # response.  This means that the requested path fit the syntactic form
            # of a registered route, but one or more of the path elements did not
            # exist.
            if ctx==None:
                return result.not_found()
            return result.returns_hal(func)(ctx)

        # we must mangle the names to avoid:
        #   "View function mapath_processoring is overwriting an existing endpoint function: process_object"
        # so - the method names can't contain < and > characters, and we append the HTTP
        # method so that /a/path/ GET and /a/path/ POST will have different method names
        # when we attach process_object.  This is the name of the method to which the Flask
        # engine dispatches.  If you don't do this, then Flask will complain that you have
        # too many 'process_object' methods
        mname=uri.replace(
            "<","_").replace(
            ">","_").replace(
            ":","_").replace(
            "/","_")+httpMethod
        process_object.__name__=mname

        # this calls process_object above, after wrapath_processoring it by a suite of wrapath_processorers.
        handler_method=hyperdns.flask.result.catch_errors(
                hyperdns.flask.crossdomain(origin='*',
                    headers=['Authorization','X-Requested-With', 'Content-Type', 'Origin'])(
                    hyperdns.flask.auth()(
                        db_commit()(
                            process_object
                ))))
        
        # now attach the docs
        handler_method.__doc__=func.__doc__
        
        # this is the equivalent of @
        api_func=hyperdns.flask._FLASKAPP.route(uri,methods=[httpMethod])(handler_method)

        
   
