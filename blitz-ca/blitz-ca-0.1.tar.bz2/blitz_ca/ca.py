#!/usr/bin/env 3python
# https://bitbucket.org/IntrepidusGroup/mallory/src/c13b232ef776b8ae206a58467a0eebd6babc225f/src/cert_auth.py
# http://docs.ganeti.org/ganeti/2.5/html/design-x509-ca.html
# http://www.openssl.org/docs/apps/x509v3_config.html

from pyasn1.codec.der.decoder import decode as decode_asn
from . import DEFAULT_KEY_TYPE, DEFAULT_KEY_SIZE, DEFAULT_DIGEST_TYPE
from OpenSSL import crypto
import logging

log = logging.getLogger('blitz-ca.ca')


def generate_certificate(db, common_name, key_id, ca=False, subject={}, extensions=[], digest=DEFAULT_DIGEST_TYPE, comment=None,
                         ca_id=None, expires_after=365):
    """if ca_id is None then its a self signed
    expires_after is in days
    """

    pkey = db.keys[key_id]['raw']
    pkey = crypto.load_privatekey(crypto.FILETYPE_ASN1, pkey)

    cert = generate_x509(common_name, pkey, ca, subject, extensions, digest, comment, X509=crypto.X509)

    cert.set_serial_number(1) # TODO: this needs to be unique
    cert.gmtime_adj_notBefore(-3600) # back date the valid time for machines with clock drift
    cert.gmtime_adj_notAfter(expires_after * 24 * 60 * 60)

    if ca_id is None: # selfsigned
        cert.set_issuer(cert.get_subject())

        cert.sign(pkey, digest)
    else:
        raise ValueError("TODO: this is wrong, get cert then retrive key from that")
        ca_key = db.keys[ca_id]['raw']
        ca_key = crypto.load_privatekey(crypto.FILETYPE_ASN1, ca_key)
    
        cert.set_issuer(ca.get_subject())

        cert.sign(ca_key, digest)

    der_cert = crypto.dump_certificate(crypto.FILETYPE_ASN1, cert)
    der_cert = bytes(der_cert)
    
    q = db.certs.insert().values(raw=der_cert, common_name=common_name, private_key=key_id, comment=comment, ca=ca is not False)
    result = db.execute(q)

    return (result.inserted_primary_key[0], cert)

def generate_request(db, common_name, key_id, ca=False, subject={}, extensions=[], digest=DEFAULT_DIGEST_TYPE, comment=None):
    pkey = db.keys[key_id]['raw']
    pkey = crypto.load_privatekey(crypto.FILETYPE_ASN1, pkey)
    
    req = generate_x509(common_name, pkey, ca, subject, extensions, digest, comment, X509=crypto.X509Req)

    req.sign(pkey, digest)

    der_req = crypto.dump_certificate_request(crypto.FILETYPE_ASN1, req)
    der_req = bytes(der_req)
    
    q = db.requests.insert().values(raw=der_req, common_name=common_name, private_key=key_id, comment=comment)
    result = db.execute(q)

    return (result.inserted_primary_key[0], req)

def generate_x509(common_name, pkey, ca=False, subject={}, extensions=[], digest=DEFAULT_DIGEST_TYPE, comment=None, X509=crypto.X509):
    """Generate a Certificate request and put it into storage
    """
    req = X509()
    req.set_pubkey(pkey)
    req.set_version(3)

    if ca is True:
        extensions.append(crypto.X509Extension(b'basicConstraints', True, b'CA:TRUE'))
    elif ca is False:
        # may as well be explicit
        extensions.append(crypto.X509Extension(b'basicConstraints', False, b'CA:FALSE'))
    elif isinstance(ca, int):
        ca = max(ca, 0) # prevent negative numbers
        ca = str(ca).encode('ASCII')
        extensions.append(crypto.X509Extension(b'basicConstraints', True, b'CA:TRUE, pathlen:' + ca))
    else:
        raise ValueError("Incorrect value for ca: {}".format(ca))
    
    # only call this once as it replaces all extensions currently in the cert
    req.add_extensions(extensions)

    subj = req.get_subject()
    for key, val in subject.items():
        try:
            setattr(subj, key, val)
        except AttributeError as err:
            raise ValueError('"{}" is not valid key for a certificate subject'.format(key)) from err
        except crypto.Error as err:
            if err.args[0][0][1] == 'ASN1_mbstring_ncopy':
                raise ValueError('Error in value, Key: "{}", Value: "{}", Error: "{}"'.format(key, val, err.args[0][0][2]))
            else:
                raise
    subj.CN = common_name

    return req    
    
def generate_key(db, typ=DEFAULT_KEY_TYPE, key_size=DEFAULT_KEY_SIZE, comment=None):
    """Generate a key and put it into storage
    
    :param conn: SQLAlchemy DB connection
    :param typ: The type of key to generate (Currently only RSA is acceptable)
    :param int key_size: The size of the key to generate in bits
    """
    pkey = crypto.PKey()
    pkey.generate_key(typ, key_size)

    der_cert = crypto.dump_privatekey(crypto.FILETYPE_ASN1, pkey)

    q = db.keys.insert().values(raw=der_cert, key_type='RSA', key_strength=key_size, comment=comment)
    result = db.execute(q)

    return (result.inserted_primary_key[0], pkey)
    
def sign_request(db, request, ca_id, digest=DEFAULT_DIGEST_TYPE, expires_after=365, comment=None):
    ca_cert = db.certs[ca_id]['raw']
    ca_cert = crypto.load_certificate(crypto.FILETYPE_ASN1, ca_cert)
    ca_key = db.certs[ca_id]['private_key']
    ca_key = db.keys[ca_key]['raw']
    ca_key = crypto.load_privatekey(crypto.FILETYPE_ASN1, ca_key)
    request = db.requests[request]['raw']
    request = crypto.load_certificate_request(crypto.FILETYPE_ASN1, request)
    
    common_name = request.get_subject().CN
    extensions = get_request_exts(request)
    
    cert = crypto.X509()
    cert.set_version(3)
    cert.set_serial_number(1) # TODO: this needs to be unique
    cert.gmtime_adj_notBefore(-3600) # back date the valid time for machines with clock drift
    cert.gmtime_adj_notAfter(expires_after * 24 * 60 * 60)

    cert.set_subject(request.get_subject())
    cert.add_extensions(extensions)
    cert.set_pubkey(request.get_pubkey())

    # we do this on the cert and not the request as the 'is_ca' 
    # does not work for X509Req
    ca = is_ca(cert)

    cert.set_issuer(ca_cert.get_subject())
    cert.sign(ca_key, digest)

    der_cert = crypto.dump_certificate(crypto.FILETYPE_ASN1, cert)
    der_cert = bytes(der_cert)
    
    q = db.certs.insert().values(raw=der_cert, common_name=common_name, comment=comment, ca=ca is not False)
    result = db.execute(q)

    return (result.inserted_primary_key[0], cert)

def is_ca(cert):
    """Is the supplied certificate a CA?
    
    If the basicConstraints extension is not found then False is returned
    
    :param X509 cert: The certficate to check
    :rtype: bool
    """
    for i in range(cert.get_extension_count()):
        ext = cert.get_extension(i)
        if ext.get_short_name() == 'basicConstraints':
            d = decode_asn(ext.get_data())
            ca = d[0][0]
            
            return ca
    return False


from OpenSSL.crypto import _lib, _ffi

def get_request_exts(req):
    """Get the extensions from a request as a list
    
    This exists as a workaround for the fact that there is no way on a 
    X509Request to get the extensions so we can display them and add them
    to the certificate before signing. we poke openssl and cryptography 
    directly, here be dragons
    
    :param X509Request req: The request to retrive the extenstions from
    :rtype: list of X509Extensions
    """
    exts_ptr = _lib.X509_REQ_get_extensions(req._req)
    count = _lib.sk_X509_EXTENSION_num(exts_ptr)
    # note there is a possible GC issue here if the extensions returned 
    # are not copies but pointers to the original object
    extensions = []
    for i in range(count):
        ext = crypto.X509Extension.__new__(crypto.X509Extension)
        ext._extension =_lib.sk_X509_EXTENSION_value(exts_ptr, i)
        extension = _lib.X509_EXTENSION_dup(ext._extension)
        ext._extension = _ffi.gc(extension, _lib.X509_EXTENSION_free)
        
        extensions.append(ext)
        
    return extensions
