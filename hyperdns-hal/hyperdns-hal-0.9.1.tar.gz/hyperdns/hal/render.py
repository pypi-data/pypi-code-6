"""Utilities for converting an object into HAL
"""
import json
import math
import datetime
import types


class EnhancedJSONEncoder(json.JSONEncoder):
    """This will automatically encode time-type objects in the
    following way:

    datetime.datetime
        Renders the year,  month, day, hour, minute, second, and microsecond

        Example::
            {
                '__type__':'datetime.datetime',
                'args':[2014,2,13,3,16,59,2325]
            }

    datetime.date
        Example::

            {
                '__type__':'datetime.datetime',
                'args':[2014,2,13,3,16,59,2325]
            }

    datetime.time

        Example::
            {
                '__type__':'datetime.datetime',
                'args':[2014,2,13,3,16,59,2325]
            }

    datetime.timedelta

        Example::
            {
                '__type__':'datetime.datetime',
                'args':[2014,2,13,3,16,59,2325]
            }

    Planned Development
        We should consider extending the default behaviour so that
        it will look for attributes like json, or _to_json and call
        that if possible.

        We should consider a standard return if super().defaul(obj)
        throws an encoding exception
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            ARGS = ('year', 'month', 'day', 'hour', 'minute',
                     'second', 'microsecond')
            return {'__type__': 'datetime.datetime',
                    'args': [getattr(obj, a) for a in ARGS]}
        elif isinstance(obj, datetime.date):
            ARGS = ('year', 'month', 'day')
            return {'__type__': 'datetime.date',
                    'args': [getattr(obj, a) for a in ARGS]}
        elif isinstance(obj, datetime.time):
            ARGS = ('hour', 'minute', 'second', 'microsecond')
            return {'__type__': 'datetime.time',
                    'args': [getattr(obj, a) for a in ARGS]}
        elif isinstance(obj, datetime.timedelta):
            ARGS = ('days', 'seconds', 'microseconds')
            return {'__type__': 'datetime.timedelta',
                    'args': [getattr(obj, a) for a in ARGS]}
        else:
            return super().default(obj)

def attach_HAL_support(class_,properties=[],resources=[],collections=[]):
    """
    Attach a method :meth:`_hal` to :class:`class_`, which will render a HAL
    instance of that class based on the identified resources, collections, and
    properties
        
    :param class_: the class to which the :meth:`_hal` method is to be attached.
    
    :param properties: a list of properties to include.  Each element is a string, and the
      value of that property will be obtained via :meth:`getattr`.  These are considered
      properties objects, and their inclusion in the HAL document will be controlled by
      the :class:`hal_render_control`'s `embed` and `depth` settings.  `None` is a valid
      value for a resource (e.g. :meth:`getattr` returns `None`)
      
    :param resources: a list of resource names.  Each element is a string, and the
      value of that resource will be obtained via :meth:`getattr`.  These are considered
      embedded objects, and their inclusion in the HAL document will be controlled by
      the :class:`hal_render_control`'s `embed` and `depth` settings.  `None` is a valid
      value for a resource (e.g. :meth:`getattr` returns `None`)
      
    :param collections: a list of tuples defining collections and indices

    """
    def render_object_as_hal_raw(self,url,hrc,cur_depth=0):
        """This is the method actually executed when you call :meth:`object._hal`
        """
        result=_render_properties(self,hrc,properties)
    
        # process the _links section
        if hrc.links:
            curies=[{
                'name':'cbase',
                'templated':True,
                'href':'%s/{rel}' % url
                },{
                'name':'sbase',
                'templated':True,
                'href':'%s/{rel}' % url
                }
            ]
            result['_links']=_render_links(self,url,hrc,curies,resources,collections)
        else:
            result['_links']={}
        
        # process embedded objects
        if hrc.embed and (cur_depth<hrc.depth or hrc.depth==0):
            result['_embedded']=_render_embedded_objects(self,url,hrc,
                                        cur_depth,resources,collections)
        else:
            result['_embedded']={}
        
        # and that's it
        return result
    setattr(class_,'_hal_raw',render_object_as_hal_raw)
    
    def render_object_as_str(self,url,hrc,cur_depth=0):
        hal=render_object_as_hal_raw(self,url,hrc,cur_depth=cur_depth)
        return json.dumps(hal,sort_keys=True,
                          cls=EnhancedJSONEncoder,
                          indent=4,
                          separators=(',', ': '))

    setattr(class_,'_hal',render_object_as_str)

class hal_render_control(object):
    """
    Properties governing how an object is rendered.  This object encapsulates the
    rendering information in one object, which is passed around the rendering
    functions.
    
    Properties Include:
    
    strict
      This boolean removes the `_class_name` and `_timestamp` properties from the
      top level object.
    
    embed
      This boolean determines whether any embedded objects will be included
      
    depth
      This integer controls the maximum depth of embedding.  When depth==0, the
      full tree is rendered, otherwise the only the first `depth` layers are
      embedded.
      
    links
      This boolean determines whether or not `_links` are included in the output.
      When False, all `_links` elements are rendered as `{}`
    
    """
    def __init__(self,strict=False,embed=False,depth=0,links=True):
        """
        :param strict: test
        :param embed: test
        """
        self.strict=strict
        self.embed=embed
        self.depth=depth
        self.links=links
        




class hal_collection(object):
    """
    Represents information about how to render a specific collection.
    
	https://phlyrestfully.readthedocs.org/en/latest/halprimer.html
    
    
    :param data: an array of data to render
    :param url: the base URL for this collection
    :param name: the name of the collection (required by HAL)
    :param keyfield: the property by which the embedded objects are present
    :param results_per_page: limitations to control how many are included.  If None, the whole
        collection is rendered, if it has a value, then the whole collection is included.  If not
        then only one page is included
    :param current_index: the start index in the collection
    """
    def __init__(self,data,url,name=None,keyfield=None,results_per_page=None,current_index=None):   
        self.data=data
        self.url=url
        self.name=name
        self.keyfield=keyfield
        self.collection_length=len(self.data)
        
        self.current_index=0
        
        # optionally set results per page, if passed in
        if results_per_page!=None:
            self.results_per_page=results_per_page
        else:
            self.results_per_page=len(self.data)
            if self.results_per_page==0:
                self.results_per_page=1
                
        self.pages=math.ceil(self.collection_length/self.results_per_page)
    
    def keyfor(self,obj):
        return str(getattr(obj,self.keyfield,None))

    def elturl(self,url,obj):
        return '%s/%s' % (url,str(getattr(obj,self.keyfield,None)))
            
    def render(self,hrc,cur_depth):
        """Renders a collection structure
        
        # structure is taken from
        # https://phlyrestfully.readthedocs.org/en/latest/halprimer.html
        
        
        """
        url='%s/%s' % (self.url,self.name)
        embedded = [datum._hal_raw(self.elturl(url,datum),hrc,cur_depth+1) for datum in self.data]
        embedded = sorted(embedded,key=lambda datum: datum[self.keyfield])
        result={
            "count": self.pages,
            "total": self.collection_length,
            "results_per_page": self.results_per_page,
            "keyfield": self.keyfield,
            "keylist": sorted([self.keyfor(datum) for datum in self.data]),
            "_embedded": {
                self.name: embedded
            }
        }
        if hrc.links:
            # @TODO this clearly needs fixing
            links={
                "self": {
                    "href": url
                },
                "first": {
                    "href": url
                },
                "prev": {
                    "href": url
                },
                "next": {
                    "href": url
                },
                "last": {
                    "href": url
                }
            }
        else:
            links={}
            
        result['_links']=links
            
        return result        

def _render_properties(source,hrc,properties):
    """return all the properties in the specification
    """
    if hrc.strict:
        result={}
    else:
        result={
            '_class_name':source.__class__.__name__,
            '_timestamp':str(datetime.datetime.now())
        }
    for prop in properties:
        v=getattr(source,prop)
        if isinstance(v,str) or v==None:
            result[prop]=v
        elif isinstance(v,object):
            if isinstance(v,bool):
                result[prop]=v
            elif isinstance(v,dict):
                result[prop]=v
            elif isinstance(v,list):
                result[prop]=v
            else:
                if hasattr(v,'json'):
                    result[prop]=v.json
                else:
                    result[prop]="%s" % v
        else:
            result[prop]=v
    return result
        

def _render_embedded_objects(source,url,hrc,cur_depth,resources,collections):
    """Render the embedded resources and collections of this object
    recursively according to the HRC (hal_rendering_control) and the current
    depth.
    
    :param source: the object whose resources and collections are rendered
    :param url: the url of this object
    :param hrc: HAL rendering control
    :param cur_depth: the current embedded resource depth
    :param resources: the single object resources to render
    :param collections: the collections to render
    """
    _embedded={}
    # now scan the object's collections
    for (c_name,c_index) in collections:
        data=getattr(source,c_name).values()
        c=hal_collection(data,url,name=c_name,keyfield=c_index)
        _embedded[c_name]=c.render(hrc,cur_depth+1) 
        
    # now embeded resources         
    for s_name in resources:
        data=getattr(source,s_name)
        if data!=None:
            c=data._hal_raw('%s/%s' % (url,s_name),hrc,cur_depth)
        else:
            c=None
        _embedded[s_name]=c             
    return _embedded

def _render_links(source,url,hrc,curies,resources,collections):
    _links={
        'self':{
            'href':url
        },
        'curies':curies
    }
    
    # emit collections as a list of keys
    for (c_name,c_index) in collections:
        coll=[]
        for datum in getattr(source,c_name).values():
            key=str(getattr(datum,c_index,None))
            coll.append({
                'href':'%s/%s/%s' % (url,c_name,key),
                'title':'%s' % key
                })
        _links['cbase:%s' % c_name]=coll
    for s_name in resources:
        _links['sbase:%s' % s_name]={
            'href':'%s' % (s_name),
            'templated':True
        }
    return _links
    


