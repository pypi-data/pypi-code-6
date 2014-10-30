import unittest
from hyperdns.hal.render import *

class PropertyBundle(object):
    def __init__(self,index=None):
        self.index=index
        self.property1="prop1"
        self.property2=["prop2"]
        self.property3={'prop':3}


class TestObject(object):
    def __init__(self):
        self.property1="prop1"
        self.property2=["prop2"]
        self.property3={'prop':3}

        self.subObject=PropertyBundle()
        
        self.map={}
        p1=PropertyBundle('index1')
        p2=PropertyBundle('index2')
        p3=PropertyBundle('index3')

        self.map[p1.index]=p1
        self.map[p2.index]=p2
        self.map[p3.index]=p3
        
class TestCase(unittest.TestCase):

    def setUp(self):
        attach_HAL_support(
            TestObject,
            properties=[
                'property1',
                'property2',
                'property3'],
            resources=['subObject'],
            collections=[('map','index')]
            )
            
        
        attach_HAL_support(
            PropertyBundle,
            properties=[
                'index',
                'property1',
                'property2',
                'property3'],
            resources=[],
            collections=[]
            )
            
        self.data=TestObject()
        
        
    def test_a00(self):
        """Check hal rendering with strict==True, no links, no embedded
        """
        hrc=hal_render_control(
               strict=True,
        	   links=False,
        	   embed=False
          )
        result=self.data._hal_raw('BASE',hrc)
        assert result=={
            "_embedded": {},
            "_links": {},
            "property1": "prop1",
            "property2": [
                "prop2"
            ],
            "property3": {
                "prop": 3
            }
        }
        
    def test_a01(self):
        """Check hal rendering with strict==False, no links, no embedded
        """
        hrc=hal_render_control(
               strict=False,
        	   links=False,
        	   embed=False
          )
        result=self.data._hal_raw('BASE',hrc)
        assert result.get('_timestamp')!=None
        result['_timestamp']="FAKETIMESTAMP"
        assert result=={
            "_class_name": "TestObject",
            "_embedded": {},
            "_links": {},
            "_timestamp": "FAKETIMESTAMP",
            "property1": "prop1",
            "property2": [
                "prop2"
            ],
            "property3": {
                "prop": 3
            }
        }
        
    def test_a03(self):
        """Check hal rendering with strict==True, but with embedded objects
        """
        hrc=hal_render_control(
               strict=True,
        	   links=False,
        	   embed=True
          )
        result = self.data._hal_raw('BASE',hrc)
        assert result=={'property2': ['prop2'], '_links': {}, 'property1': 'prop1', '_embedded': {'subObject': {'property3': {'prop': 3}, 'property2': ['prop2'], '_embedded': {}, '_links': {}, 'property1': 'prop1', 'index': None}, 'map': {'keyfield': 'index', 'keylist': ['index1', 'index2', 'index3'], 'count': 1, 'total': 3, 'results_per_page': 3, '_links': {}, '_embedded': {'map': [{'property3': {'prop': 3}, 'property2': ['prop2'], '_embedded': {}, '_links': {}, 'property1': 'prop1', 'index': 'index1'}, {'property3': {'prop': 3}, 'property2': ['prop2'], '_embedded': {}, '_links': {}, 'property1': 'prop1', 'index': 'index2'}, {'property3': {'prop': 3}, 'property2': ['prop2'], '_embedded': {}, '_links': {}, 'property1': 'prop1', 'index': 'index3'}]}}}, 'property3': {'prop': 3}}
        
        
        
