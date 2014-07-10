
from dns.rdatatype import NONE 
from dns.rdatatype import A
from dns.rdatatype import NS
from dns.rdatatype import MD
from dns.rdatatype import MF
from dns.rdatatype import CNAME
from dns.rdatatype import SOA
from dns.rdatatype import MB
from dns.rdatatype import MG
from dns.rdatatype import MR
from dns.rdatatype import NULL
from dns.rdatatype import WKS
from dns.rdatatype import PTR
from dns.rdatatype import HINFO
from dns.rdatatype import MINFO
from dns.rdatatype import MX
from dns.rdatatype import TXT
from dns.rdatatype import RP
from dns.rdatatype import AFSDB
from dns.rdatatype import X25
from dns.rdatatype import ISDN
from dns.rdatatype import RT
from dns.rdatatype import NSAP
from dns.rdatatype import NSAP_PTR
from dns.rdatatype import SIG
from dns.rdatatype import KEY
from dns.rdatatype import PX
from dns.rdatatype import GPOS
from dns.rdatatype import AAAA
from dns.rdatatype import LOC
from dns.rdatatype import NXT
from dns.rdatatype import SRV
from dns.rdatatype import NAPTR
from dns.rdatatype import KX
from dns.rdatatype import CERT
from dns.rdatatype import A6
from dns.rdatatype import DNAME
from dns.rdatatype import OPT
from dns.rdatatype import APL
from dns.rdatatype import DS
from dns.rdatatype import SSHFP
from dns.rdatatype import IPSECKEY
from dns.rdatatype import RRSIG
from dns.rdatatype import NSEC
from dns.rdatatype import DNSKEY
from dns.rdatatype import DHCID
from dns.rdatatype import NSEC3
from dns.rdatatype import NSEC3PARAM
from dns.rdatatype import TLSA
from dns.rdatatype import HIP
from dns.rdatatype import SPF
from dns.rdatatype import UNSPEC
from dns.rdatatype import TKEY
from dns.rdatatype import TSIG
from dns.rdatatype import IXFR
from dns.rdatatype import AXFR
from dns.rdatatype import MAILB
from dns.rdatatype import MAILA
from dns.rdatatype import ANY
from dns.rdatatype import TA
from dns.rdatatype import DLV

import dns.rdatatype as dnstypes

from dns.rdataclass import ANY as ANY_CLASS
from dns.rdataclass import CH as CH_CLASS
from dns.rdataclass import HS as HS_CLASS
from dns.rdataclass import IN as IN_CLASS
from dns.rdataclass import NONE as NO_CLASS
from dns.rdataclass import RESERVED0 as RESERVED_CLASS
    
DEFAULT_NAMESERVER="8.8.8.8"

def rd_type_as_int(text):
    """Convert text into a DNS rdata type value.
    @param text: the text
    @type text: string
    @raises dns.rdatatype.UnknownRdatatype: the type is unknown
    @raises ValueError: the rdata type value is not >= 0 and <= 65535
    @rtype: int"""
    
    text=("%s" % text).strip().upper()
    value = dnstypes._by_text.get(text.upper())
    if value is None:
        value = int(text)
        if value < 0 or value > 65535:
            raise ValueError("type must be between >= 0 and <= 65535")
    return value

def rd_type_as_str(value):
    """Convert a DNS rdata type to text.
    @param value: the rdata type value
    @type value: int
    @raises ValueError: the rdata type value is not >= 0 and <= 65535
    @rtype: string"""

    value=rd_type_as_int(value)
    if value < 0 or value > 65535:
        raise ValueError("type must be between >= 0 and <= 65535")
    text = dnstypes._by_value.get(value)
    if text is None:
        raise ValueError("type '%s' is not recognized" % text)        
    return text


def rd_type_is_singleton(rdtype):
    """True if the type is a singleton.
    @param rdtype: the type
    @type rdtype: int ot text
    @rtype: bool"""
    if dnstypes._singletons.has_key(rd_type_as_str(rdtype)):
        return True
    return False

def rd_class_as_str(rdclass):
    s=str(rdclass).strip().upper()
    if s!='1' and s!='IN':
        raise ValueError("Unsupported class '%s'" % rdclass)
    return 'IN'
    
def rd_class_as_int(rdclass):
    s=str(rdclass).strip().upper()
    if s!='1' and s!='IN':
        raise ValueError("Unsupported class '%s'" % rdclass)
    return 1

from .names import (
    dotify,
    undotify,
    splitHostFqdn
    )
from .spec import (
    RecordSpec,
    MalformedRecordException,
    MalformedTTLException
    )
from .tld import refresh_tld_list
from .tld import validate_tld
from .lookups import (
    get_address_for_nameserver,
    query_nameserver,
    full_report_as_json,
    quick_lookup
    )
from .zonefiles import translate_zonefiletext_to_json
from .zonefiles import translate_json_to_zonefiletext

