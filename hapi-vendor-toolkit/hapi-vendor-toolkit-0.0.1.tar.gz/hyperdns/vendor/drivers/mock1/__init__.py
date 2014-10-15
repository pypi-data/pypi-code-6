
from hyperdns.vendor.drivers.mock import HyperDNSDriver as Base

class HyperDNSDriver(Base):
    vkey='mock1'
    name='Mock Subvendor 1'
    info={
        'vendor':'HyperDNS Test',
        'service':'Simple Mock Driver - alternate 1',
        'description':'This is a mock driver for %s' % vkey,
        'settings':['username','password','persistence_file'],
        'angular':{
            'username': {
                'label':'Mock Username',
                'type':'text',
                'placeholder':"User Name"
            },
            'password': {
                'label':'Mock Password',
                'type':'password',
                'placeholder':"Password (should be same as username)"
            },
            'persistence_file': {
                'label':'',
                'type':'hidden',
                'placeholder':""
            }
        }
    }
