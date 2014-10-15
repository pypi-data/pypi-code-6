#
"""Utilities for converting an object into HAL
"""
import json
import math
import datetime

def _render_wrapper(obj,url,details):

    if hasattr(obj,'_hal'):
        return obj._hal(url,details=details)
    
    raise Exception("%s" % (str(obj)))


class hal_collection(object):
    """
    Represents information about how to 
    Example Usage
    
        return hyperdns.hal.render.collection(  data=blah,
                                                parent=obj,
                                                name='',
                                                keyfield='a')
    """
    def __init__(self,data=[],parent=None,name=None,keyfield=None):   
        assert parent!=None 
        self.data=data
        self.parent=parent
        self.name=name
        self.keyfield=keyfield
        self.collection_length=len(self.data)
        self.results_per_page=len(self.data)
        if self.results_per_page==0:
            self.results_per_page=1
        self.pages=math.ceil(self.collection_length/self.results_per_page)
    
    def keyfor(self,obj):
        return str(getattr(obj,self.keyfield,None))

    def elturl(self,url,obj):
        return '%s/%s' % (url,str(getattr(obj,self.keyfield,None)))

    @property
    def as_keylist(self):
        return [self.keyfor(datum) for datum in self.data]
        
    @property
    def as_map(self):
        result={}
        for datum in self.data:
            result[self.keyfor(datum)]=datum
        return result
    
    def _hal(self,url,details=True):
        """Renders a collection structure
        
        # structure is taken from
        # https://phlyrestfully.readthedocs.org/en/latest/halprimer.html
        
        
        """
        url='%s/%s' % (url,self.name)
        result={
            "_links": {
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
            },
            "count": self.pages,
            "total": self.collection_length,
            "results_per_page": self.results_per_page,
            "keyfield": self.keyfield,
            "keylist": self.as_keylist,
            "_embedded": {
                self.name: [_render_wrapper(datum,self.elturl(url,datum),details) for datum in self.data]
            }
        }
        return result

class hal_array(object):
    """
    """
    def __init__(self,data=[],name='array'):   
        self.data=data
        self.name=name
        self.collection_length=len(self.data)
        self.results_per_page=len(self.data)
        if self.results_per_page==0:
            self.results_per_page=1
        self.pages=math.ceil(self.collection_length/self.results_per_page)
        
    def _hal(self,url,details=False):
        """Renders a collection structure
        
        # structure is taken from
        # https://phlyrestfully.readthedocs.org/en/latest/halprimer.html
        
        
        """
        result={
            "_links": {
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
            },
            "count": self.pages,
            "total": self.collection_length,
            "results_per_page": self.results_per_page,
            "_embedded": {
                self.name: [_render_wrapper(datum,url,details) for datum in self.data]
            }
        }
        return result
              
class hal_object(object):
    """Methods that return a hal object will first wrap it with this
    wrapper, which controls the rendering of the object as HAL by determining
    which scalaras, collections, and properties are included, as well as
    whether or not the embedded information is included.
    """
    def __init__(self,data=None,scalars=[],collections=[],properties=[]):
        self.data=data
        self.class_=data.__class__
        self.scalars=scalars
        self.collections=collections
        self.properties=properties
                  
    def _hal_embedded(self,url,embed_details=True):
        """Return a map of embedded objects
        """
        _embedded={}
        if embed_details:
            for (c_name,c_defn,c_index) in self.collections:
                data=getattr(self.data,c_name).values()
                c=hal_collection(data=data,parent=self.data,name=c_name,keyfield=c_index)
                _embedded[c_name]=c._hal(url)                
            for (s_name,s_defn) in self.scalars:
                data=getattr(self.data,s_name)
                if data!=None:
                    #c=hal_object(data=data)._hal('%s/%s' % (url,s_name))
                    c=data._hal('%s/%s' % (url,s_name))
                else:
                    c=None
                _embedded[s_name]=c             
        return _embedded
        
    def _hal_curies(self,url):
        _curies=[{
            'name':'cbase',
            'templated':True,
            'href':'%s/{rel}' % url
            },{
            'name':'sbase',
            'templated':True,
            'href':'%s/{rel}' % url
            }
        ]
        return _curies

    def _hal_links(self,url):
        _links={
            'self':{
                'href':url
            },
            'curies':self._hal_curies(url)
        }
        
        # emit collections as a list of keys
        for (c_name,c_defn,c_index) in self.collections:
            coll=[]
            for datum in getattr(self.data,c_name).values():
                key=str(getattr(datum,c_index,None))
                coll.append({
                    'href':'%s/%s/%s' % (url,c_name,key),
                    'title':'%s' % key
                    })
            _links['cbase:%s' % c_name]=coll
        for (s_name,s_defn) in self.scalars:
            _links['sbase:%s' % s_name]={
                'href':'%s' % (s_name),
                'templated':True
            }
        return _links
        
    def _hal_props(self):
        """return all the properties in the specification
        """
        result={
            '_class_name':self.data.__class__.__name__,
            '_timestamp':str(datetime.datetime.now())
        }
        for prop,attr in self.properties:
            v=getattr(self.data,prop)
            #print("Encoding property %s:%s, type=%s" % (prop,dir(attr.__class__),v.__class__))
            if isinstance(v,str) or v==None:
                #print("Prop %s tested as (string, or none)" % prop)
                result[prop]=v
            elif isinstance(v,object):
                if isinstance(v,bool):
                    result[prop]=v
                elif isinstance(v,dict):
                    result[prop]=v
                elif isinstance(v,list):
                    #print("Prop %s is a list" % prop)
                    #for elt in v:
                    #    print("Prop %s, elt=%s, type=%s" % (prop,elt,type(elt)))
                    result[prop]=v
                else:
                    if hasattr(v,'json'):
                        result[prop]=v.json
                    else:
                        result[prop]="%s" % v
            else:
                result[prop]=v
        return result
        
    def _hal(self,url=None,details=True):
        """This is called by the simple_halifier
        """
        result=self._hal_props()
        result['_links']=self._hal_links(url)
        result['_embedded']=self._hal_embedded(url,embed_details=details)        
        return result

class hal_json(object):
    """Returns a simple json object as HAL
    """
    def __init__(self,data=None):
        self.data=data
        
    def _hal(self,url=None,details=True):
        """This is called by the simple_halifier
        """
        result=self.data
        if isinstance(self,dict):
            result['_links']={
                'self':{
                    'href':url
                }
            }
        return result        

import types
class hal_spec(object):
    """
    """
    
    def __init__(self,class_,scalars=[],collections=[],properties=[]):
        self.class_=class_
        self.scalars=scalars
        self.collections=collections
        self.properties=properties
        
    def __repr__(self):
        return "HAL_spec(%s)" % (self.class_.__name__)


def attach_HAL_support(spec):
    
    def _hal(self,url=None,details=True):
        """This is called by the simple_halifier
        """
        r=hal_object(data=self,scalars=spec.scalars,
            collections=spec.collections,properties=spec.properties)
        return r._hal(url)
    setattr(spec.class_,'_hal',_hal)

#
