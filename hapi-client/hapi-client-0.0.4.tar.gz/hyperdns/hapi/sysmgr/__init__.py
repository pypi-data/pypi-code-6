"""   
"""
import re
from hyperdns.hal.navigator import HALRoot

class SHAPI(HALRoot):
    """System management client - almost same as client, but with different
    root - this is at <APP>/system instead of <APP>/my
    """
    def __init__(self,jwt,baseUrl=None):
        super(SHAPI,self).__init__(jwt,baseUrl)

from hyperdns.hapi.client.account import *
from hyperdns.hapi.client.vendor import *
from hyperdns.hapi.client.zone import *
