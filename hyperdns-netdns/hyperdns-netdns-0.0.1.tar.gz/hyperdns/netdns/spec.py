import json
import ipaddress
import hyperdns.netdns
from hyperdns.netdns import rd_type_as_str
from hyperdns.netdns import rd_type_as_int
from hyperdns.netdns import rd_class_as_str
from hyperdns.netdns import rd_class_as_int
from hyperdns.netdns import IN_CLASS

class MalformedRecordException(Exception):
    pass
class MalformedTTLException(MalformedRecordException):
    pass
class MalformedResourceDataType(MalformedRecordException):
    pass
    
DEFAULT_TTL=200

class RecordSpec(object):
    
    def __init__(self,json=None,text=None,wire=None,ttl=None,rdata=None,rdtype=None,rdclass=None):
        # integer
        self._ttl=ttl
        # string/bolums
        self._rdata=rdata
        # short int, but exported as text
        if rdtype!=None:
            self._rdtype=rd_type_as_int(rdtype)
        # short in, but exported as text
        if rdclass!=None:
            self._rdclass=rd_class_as_int(rdclass)
        else:
            self._rdclass=IN_CLASS
            
        if json!=None:
            self.json=json
        elif text!=None:
            raise Exception('Implement text form')
        elif wire!=None:
            raise Exception('Implement wire form')
        else:
            assert ttl!=None and rdata!=None and rdtype!=None
            
    @property
    def key(self):
        return "{%s}{%s}{%s}{%s}" % (self._rdata,self._ttl,self._rdtype,self._rdclass)

    @property
    def singleton(self):
        return rd_type_is_singleton(self._rdtype)
    def __eq__(self,other):
        if isinstance(other,self.__class__):
            return self._ttl==other._ttl            \
                and self._rdata==other._rdata       \
                and self._rdtype==other._rdtype     \
                and self._rdclass==other._rdclass
        elif isinstance(other,dict):            
            return self._ttl==other.get('ttl',None)       \
                and self._rdata==other.get('rdata',None)  \
                and self._rdtype==rd_type_as_int(other.get('type',None))  \
                and self._rdclass==rd_class_as_int(other.get('class',None))
        else:
            print("Unknown type")
            return False
        
    def __ne__(self,other):
        return not self.__eq__(other)
 
    @property
    def ttl(self):
        return self._ttl
        
    @ttl.setter
    def ttl(self,value):
        """Assign a ttl value as integer or BIND 8 units.
        
        Example:
             spec.ttl=200
             spec.ttl='1w3m'

        @raises MalformedTTLException: the TTL is not well-formed 
        @rtype: int 
        """
        if isinstance(value,int) or isinstance(value,long):
            newval=value
        else:
            value=str(value).strip().lower()
            if value.isdigit(): 
                newval = long(text)
            else:
                if not value[0].isdigit():
                    raise MalformedTTLException('Initial character must be numeric')

                newval= 0
                current = 0
                for c in value:
                    if c.isdigit():
                        current = 10 * current + long(c)
                    else:
                        factors={
                            'w':604800,
                            'd':86400,
                            'm':60,
                            's':1
                        }
                        factor=factors.get(c)
                        if factor==None:
                            raise MalformedTTLException("unknown unit '%s'" % c)
                            
                        newval = newval + current * factor
                        current = 0
                if current != 0:
                    raise MalformedTTLException('BIND8 TTLs must end in units')
        # final check before assignment    
        if newval < 0 or newval > 2147483647: 
            raise MalformedTTLException("TTL should be between 0 and 2^31 - 1 (inclusive), not %s" % newval) 
        self._ttl=newval
        return self._ttl
   
    @property
    def rdata(self):
        return self._rdata
        
    @rdata.setter
    def rdata(self,value):
        """Set rdata according to record type
        @TODO - zoiks, this is complex, bypassing with simple assignment now"""
        self._rdata=value
        return self._rdata
 
        
    @property
    def rdtype(self):
        return self.num_rdtype
        
    @property
    def num_rdtype(self):
        return self._rdtype
        
    @property
    def str_rdtype(self):
        return rd_type_as_str(self._rdtype)
        
    @rdtype.setter
    def rdtype(self,value):
        if isinstance(value,int) or isinstance(value,long):
            if rd_type_as_int(value)==None:
                raise MalformedResourceDataType("Do not recognize type %s" % value)
            self._rdtype=int(value)
        else:
            value=str(value).strip().upper()
            self._rdtype=rd_type_as_int(value)


        
    @property
    def rdclass(self):
        return self.num_rdclass
        
    @property
    def num_rdclass(self):
        return 1
        
    @property
    def str_rdclass(self):
        return 'IN'
        
    @rdclass.setter
    def rdclass(self,value):
        pass
        
    @property
    def json(self):
        return {
            'ttl':self._ttl,
            'rdata':self._rdata,
            'type':self.str_rdtype,
            'class':self.str_rdclass
        }

    @json.setter
    def json(self,value):
        try:
            ttl=value.get('ttl',DEFAULT_TTL)
            rdata=value.get('rdata')
            rdtype=value.get('type')
            rdclass=value.get('class',IN_CLASS)
            
            assert ttl!=None and rdata!=None and rdtype!=None and rdclass!=None
            self.ttl=ttl
            self.rdata=rdata
            self.rdtype=rd_type_as_int(rdtype)
            self.rdclass=rd_class_as_int(rdclass)
        except ValueError as E:
            msg="ValueError:%s" % E
            raise MalformedRecordException(msg)
        except KeyError as E:
            raise MalformedRecordException(E)
        except MalformedTTLException:
            raise
        except Exception as E:
            print(E)
            raise MalformedRecordException()
            
        return self.json

    def __repr__(self):
        return json.dumps(self.json,sort_keys=True)
    
    def __getitem__(self,key):
        if key=='ttl':
            return self.ttl
        elif key=='rdata':
            return self.rdata
        elif key=='type':
            return self.rdtype
        elif key=='class':
            return self.rdclass
        else:
            raise AttributeError('No such attribute:%s' % key)
            
    def __setitem__(self,key,value):
        if key=='ttl':
            self.ttl=value
        elif key=='rdata':
            self.rdata=value
        elif key=='type' or key=='rdtype':
            self.rdtype=value
        elif key=='class' or key=='rdclass':
            self.rdclass=value
        else:
            raise AttributeError('No such attribute:%s' % key)
         
         
         
def ipv4_a_record(ip,ttl=86400):
    """Return a record spec for an IPV4 A Record or throw a ValueError
    if the ip is malformed.
    """
    return RecordSpec(json={
        'ttl':ttl,
        'rdata':str(ipaddress.ip_address(ip)),
        'type':hyperdns.netdns.A,
        'class':IN_CLASS
    })
            