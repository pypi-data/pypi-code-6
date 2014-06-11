'''RRDA Rest DNS API client'''

import drest

# Getting resources records
ENDPOINT = (
    (['GET'], 'A', '/a',
     'Get Host Address.'),
    (['GET'], 'AAAA', '/aaaa',
     'Get IPv6 Host Address.'),
    (['GET'], 'CERT', '/cert',
     'Get Certificate.'),
    (['GET'], 'CNAME', '/cname',
     'Get Canonical Name.'),
    (['GET'], 'DHCID', '/dhcid',
     'Get DHCP Identifier.'),
    (['GET'], 'DLV', '/dlv',
     'Get DNSSEC Lookaside Validation record.'),
    (['GET'], 'DNAME', '/dname',
     'Get Delegation name.'),
    (['GET'], 'DNSKEY', '/dnskey',
     'Get DNS Key record.'),
    (['GET'], 'DS', '/ds',
     'Get Delegation Signer.'),
    (['GET'], 'HINFO', '/hinfo',
     'Get Host Information.'),
    (['GET'], 'HIP', '/hip',
     'Get Host Identity Protocol.'),
    (['GET'], 'IPSECKEY', '/ipseckey',
     'Get IPSec Key.'),
    (['GET'], 'KX', '/kx',
     'Get Key eXchanger record.'),
    (['GET'], 'LOC', '/loc',
     'Get Location record.'),
    (['GET'], 'MX', '/mx',
     'Get Mail Exchange record.'),
    (['GET'], 'NAPTR', '/naptr',
     'Get Name Authority Pointer.'),
    (['GET'], 'NS', '/ns',
     'Get Name Servers.'),
    (['GET'], 'NSEC', '/nsec',
     'Get Next-Secure record.'),
    (['GET'], 'NSEC3', '/nsec3',
     'Get NSEC record version 3.'),
    (['GET'], 'NSEC3PARAM', '/nsec3param',
     'Get NSEC3 parameters.'),
    (['GET'], 'OPT', '/opt',
     'Get Option record.'),
    (['GET'], 'PTR', '/ptr',
     'Get Pointer record.'),
    (['GET'], 'RRSIG', '/rrsig',
     'Get Resource Records Signature.'),
    (['GET'], 'SOA', '/soa',
     'Get Start of Authority.'),
    (['GET'], 'SPF', '/spf',
     'Get Sender Policy Framework.'),
    (['GET'], 'SRV', '/srv',
     'Get Service Locator.'),
    (['GET'], 'SSHFP', '/sshfp',
     'Get SSH Public Key Fingerprint.'),
    (['GET'], 'TA', '/ta',
     'Get DNSSEC Trust Authorities.'),
    (['GET'], 'TALINK', '/talink',
     'Get Trust Anchor LINK.'),
    (['GET'], 'TLSA', '/tlsa',
     'Get TLSA records.'),
    (['GET'], 'TXT', '/txt',
     'Get Text record.'),
)

class RRDAAPI(drest.API):
    '''Interact with RRDA's REST DNS API'''
    def __init__(self, *args, **kwargs):
        super(RRDAAPI, self).__init__(*args, **kwargs)
        for methods, name, path, desc in ENDPOINT:
            self.add_resource(name, path=path) 
            docstring = '[{methods}] {desc}'.format(
                methods='|'.join(methods),
                desc=desc)
            getattr(self, name).__doc__ = docstring

    class Meta:
        '''Override default arguments'''
        #pylint: disable-msg=W0232
        #pylint: disable-msg=R0903
        trailing_slash = False
        timeout = 60
