import unittest
from hyperdns.hal.render import *
import re

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
        actual=self.data._hal('BASE',hrc)
        expected="""{
    "_embedded": {},
    "_links": {},
    "property1": "prop1",
    "property2": [
        "prop2"
    ],
    "property3": {
        "prop": 3
    }
}"""
        assert actual==expected
        
    def test_a01(self):
        """Check hal rendering with strict==False, no links, no embedded
        """
        hrc=hal_render_control(
               strict=False,
               links=False,
               embed=False
          )
        actual=self.data._hal('BASE',hrc)
        actual = re.sub('"_timestamp": "[^"]*"','"_timestamp": "FAKETIMESTAMP"',actual)
        expected="""{
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
}"""



        assert actual==expected
        
    def test_a03(self):
        """Check hal rendering with strict==True, but with embedded objects
        """
        hrc=hal_render_control(
               strict=True,
               links=False,
               embed=True
          )
        actual = self.data._hal('BASE',hrc)
        expected="""{
    "_embedded": {
        "map": {
            "_embedded": {
                "map": [
                    {
                        "_embedded": {},
                        "_links": {},
                        "index": "index1",
                        "property1": "prop1",
                        "property2": [
                            "prop2"
                        ],
                        "property3": {
                            "prop": 3
                        }
                    },
                    {
                        "_embedded": {},
                        "_links": {},
                        "index": "index2",
                        "property1": "prop1",
                        "property2": [
                            "prop2"
                        ],
                        "property3": {
                            "prop": 3
                        }
                    },
                    {
                        "_embedded": {},
                        "_links": {},
                        "index": "index3",
                        "property1": "prop1",
                        "property2": [
                            "prop2"
                        ],
                        "property3": {
                            "prop": 3
                        }
                    }
                ]
            },
            "_links": {},
            "count": 1,
            "keyfield": "index",
            "keylist": [
                "index1",
                "index2",
                "index3"
            ],
            "results_per_page": 3,
            "total": 3
        },
        "subObject": {
            "_embedded": {},
            "_links": {},
            "index": null,
            "property1": "prop1",
            "property2": [
                "prop2"
            ],
            "property3": {
                "prop": 3
            }
        }
    },
    "_links": {},
    "property1": "prop1",
    "property2": [
        "prop2"
    ],
    "property3": {
        "prop": 3
    }
}"""

        assert actual==expected
