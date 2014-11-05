#!/usr/bin/env 3python

# https://bitbucket.org/IntrepidusGroup/mallory/src/c13b232ef776b8ae206a58467a0eebd6babc225f/src/cert_auth.py
# http://docs.ganeti.org/ganeti/2.5/html/design-x509-ca.html
# http://www.openssl.org/docs/apps/x509v3_config.html

from .ca import generate_certificate, generate_request, generate_key, sign_request
from .database import metadata
from .database import list_cert_authorities
from .database import Database
from argparse import ArgumentParser, ONE_OR_MORE, ZERO_OR_MORE, OPTIONAL
from OpenSSL.crypto import dump_certificate_request, load_certificate_request
from OpenSSL.crypto import dump_certificate, load_certificate
from OpenSSL.crypto import dump_privatekey, load_privatekey
from OpenSSL.crypto import TYPE_DSA, TYPE_RSA, FILETYPE_ASN1, FILETYPE_PEM
from OpenSSL.crypto import X509Extension
from OpenSSL import crypto
from sqlalchemy import create_engine
from .util import short_string
import humanize
import logging
import sys, os

from . import DEFAULT_KEY_TYPE, DEFAULT_KEY_SIZE, DEFAULT_DIGEST_TYPE
from . import DEFAULT_DB

log = logging.getLogger('blitz-ca.cmdline')

key_usage={'digitalsignature': 'digitalSignature',
           'nonrepudiation':   'nonRepudiation',
           'keyencipherment':  'keyEncipherment',
           'dataencipherment': 'dataEncipherment',
           'keyagreement':     'keyAgreement',
           'keycertsign':      'keyCertSign',
           'crlsign':          'cRLSign',
           'encipheronly':     'encipherOnly',
           'decipheronly':     'decipherOnly',
           }
e_key_usage={'serverauth':     'serverAuth',
             'clientauth':     'clientAuth',
             'codesigning':    'codeSigning',
             'emailprotection':'emailProtection',
             'timestamping':   'timeStamping',
             'mscodeind':      'msCodeInd',
             'mscodecom':      'msCodeCom',
             'msctlsign':      'msCTLSign',
             'mssgc':          'msSGC',
             'msefs':          'msEFS',
             'nssgc':          'nsSGC',
             }

def main(argv=sys.argv[1:]):
    args = ArgumentParser()
    args.add_argument('-f', '--file', metavar="FILE", default=DEFAULT_DB,
        help="The file containing the certificate store")
    args.add_argument('-H', '--human', default=False, action='store_true',
        help="Use human readable numbers and times (Default: %(default)s)")
    args.add_argument('-v', '--verbose', action="count", default=0,
        help="Increase the verbosity of logging (can be specified more than once)")
#    args.set_defaults(command=None, sub_command=None)
    args.set_defaults(usage=[], san=[], extension=[], subject=None, prompt=False, args=[])
    subs = args.add_subparsers()
    
    #### Cert ####
    cert_cmd = subs.add_parser('cert', aliases=['certs', 'certificate', 'certificates'], help="Generate and display Certificates and Certificate Authorities")
    cert_subs = cert_cmd.add_subparsers(dest='sub_command')
    
    cert_cmd.add_argument('-k', '--key', type=int,
        help="Specify which key to use with the certificate")
    cert_cmd.add_argument('-c', '--csr', metavar="CSR", type=int,
        help="Specify which csr/key to use with the certificate request")
    cert_cmd.add_argument('-a', '--ca', default=False, action="store_true",
        help="Only display certificate authorities")
    cert_cmd.add_argument('-i', '--id', metavar='ID', dest='cert_id', type=int,
        help="If specified, the ID of the certificate to display")
    cert_cmd.set_defaults(command='cert')
    
    cert_gen = cert_subs.add_parser('new', help="Generate a new Certificate")
    cert_gen.add_argument('-k', '--key', type=int,
        help="Specify which key to use with the certificate.")
    cert_gen.add_argument('-c', '--cert', type=int,
        help="Specify which cert/key to use with the certificate.")
    cert_gen.add_argument('-P', '--parent', type=int,
        help="Specify which cert should be used to sign this certificate. if not specified then the certificate is assumed to be self signed")
    cert_gen.add_argument('-d', '--digest', choices={'sha1', 'sha256', 'sha512'}, default=DEFAULT_DIGEST_TYPE,
        help="Digest algorithm to use to sign the certificate (Default: %(default)s)")
    cert_gen.add_argument('-b', '--bits', default=DEFAULT_KEY_SIZE, type=int,
        help="Key strength to use when generating a key (Default: %(default)s)")
    cert_gen.add_argument('-t', '--type', choices={'rsa', 'dsa'}, default="rsa",
        help="What type of key to generate (default: %(default)s)")
    cert_gen.add_argument('-a', '--ca', default=False, const=True, nargs=OPTIONAL, type=int, metavar="CA-DEPTH",
        help="Request that this certificate be capable of signing other certificates. If an integer argument is supplied "
        "Then this is used as the maximum number of child Certificate Authorities beneath this certificate. If zero "
        "Then this certificate is incapable of issuing CA certificates" )
    cert_gen.add_argument('-D', '--days', type=int, default=365,
        help="The amount of days the certificate is valid for (Default: %(default)s days)")
    cert_gen.add_argument('-p', '--prompt', default=False, action='store_true',
        help="Prompt for common subject values (countryName, stateOrProvinceName, localityName, organizationName, organizationalUnitName, emailAddress)")
    cert_gen.add_argument('-u', '--usage', default=[], action='append', 
        choices=list(key_usage.keys()) + list(e_key_usage.keys()),
        help="Specify the key usage, can be specified multiple times.")
    cert_gen.add_argument('-e', '--extension', default=[], action="append",
        help='x509 Extension in the form "key=value", can be specified multiple times. If the key starts with "critical," then '
             'the extension is assumed to be a "critical" extension and the correct flags for that extension will be set')
    cert_gen.add_argument('-C', '--comment', type=short_string(64), help="Add extra notes to the Database.")
    cert_gen.add_argument('args', nargs=ONE_OR_MORE, metavar='ARG',
        help="The common name of the entity the certificate identifies (eg email address or hostname). "
             "If more than one argument is provided they will be converted to Subject Alternative names")

    #### CSR ####
    csr_cmd = subs.add_parser('req', aliases=['reqs', 'request', 'requests'], help="Generate and Sign Certificate Requests")
    csr_cmd.add_argument('-i', '--id', metavar='ID', dest='req_id', type=int,
        help="If specified, the ID of the certificate signing request to display.")
    csr_cmd.set_defaults(command='req')
    csr_subs = csr_cmd.add_subparsers(dest='sub_command')
    
    csr_gen = csr_subs.add_parser('new', help="Generate a new Certificate Signing Request")
    csr_gen.add_argument('-k', '--key', type=int,
        help="Specify which key to use with the certificate request.")
    csr_gen.add_argument('-c', '--cert', type=int,
        help="Specify which cert/key to use with the certificate request.")
    csr_gen.add_argument('-d', '--digest', choices={'sha1', 'sha256', 'sha512'}, default=DEFAULT_DIGEST_TYPE,
        help="Digest algorithm to use to sign the certificate (Default: %(default)s)")
    csr_gen.add_argument('-b', '--bits', default=DEFAULT_KEY_SIZE, type=int,
        help="Key strength to use when generating a key (Default: %(default)s)")
    csr_gen.add_argument('-t', '--type', choices={'rsa', 'dsa'}, default="rsa",
        help="What type of key to generate (default: %(default)s)")
    csr_gen.add_argument('-a', '--ca', default=False, const=True, nargs=OPTIONAL, type=int, metavar="CA-DEPTH",
        help="Request that this certificate be capable of signing other certificates. If an integer argument is supplied "
        "Then this is used as the maximum number of child Certificate Authorities beneath this certificate. If zero "
        "Then this certificate is incapable of issuing CA certificates" )
    csr_gen.add_argument('-p', '--prompt', default=False, action='store_true',
        help="Prompt for common subject values (countryName, stateOrProvinceName, localityName, organizationName, organizationalUnitName, emailAddress)")
    csr_gen.add_argument('-u', '--usage', default=[], action='append', 
        choices=list(key_usage.keys()) + list(e_key_usage.keys()),
        help="Specify the key usage, can be specified multiple times.")
    csr_gen.add_argument('-e', '--extension', default=[], action="append",
        help='x509 Extension in the form "key=value", can be specified multiple times. If the key starts with "critical," then '
             'the extension is assumed to be a "critical" extension and the correct flags for that extension will be set')
    csr_gen.add_argument('-C', '--comment', type=short_string(64), help="Add extra notes to the Database.")
    csr_gen.add_argument('args', nargs=ONE_OR_MORE, metavar='ARG',
        help="The common name of the entity the certificate identifies (eg email address or hostname). "
             "If more than one argument is provided they will be converted to Subject Alternative names")
    
    sign_cmd = csr_subs.add_parser("sign", help="Sign a certificate")
    sign_cmd.add_argument('req', type=int, 
        help="The request to sign")
    sign_cmd.add_argument('ca', type=int,
        help="The CA to use to sign the request")
    
    #### Keys ####
    keys_cmd = subs.add_parser('key', aliases=['keys'], help="Generate and display keys")
    keys_cmd.add_argument('-d', '--days', type=int, default=365,
        help="Ammount of days a key is allowed to exist before being considered 'expired'")
    keys_cmd.add_argument('-i', '--id', metavar='ID',  dest='key_id', type=int,
        help="If specified, the ID of the key to display")
    keys_cmd.set_defaults(command='keys')
    
    options = args.parse_args(argv)

    options.verbose = min(5, options.verbose)
    log.addHandler(logging.StreamHandler())
    log.setLevel({0:logging.ERROR,
                  1:logging.CRITICAL,
                  2:logging.ERROR,
                  3:logging.WARN,
                  4:logging.INFO,
                  5:logging.DEBUG,
                 }[options.verbose])

    DEBUG = options.verbose >= 5 # logging.DEBUG
    log.info("Debug flag: %s", DEBUG)

    extensions = []

    k = [key_usage[key] for key in options.usage if key in key_usage]
    if k:
        val = ','.join(k)
        ext = X509Extension(b'keyUsage', True, val.encode('ASCII'))
        extensions.append(ext)
        
    e_k = [e_key_usage[key] for key in options.usage if key in e_key_usage]
    if e_k:
        val = ','.join(e_k)
        ext = X509Extension(b'extendedKeyUsage', True, val.encode('ASCII'))
        extensions.append(ext)

    if options.args:
        common_name = options.args[0]
    
    subject = {}
    vals = []
    for fragment in options.args[1:]:
        if '=' in fragment:
            # this is a value for a subject
            key, value = fragment.split("=")
            key = key.strip()
            value = value.strip()

            if key.lower() in ('cn', 'commonname'):
                print("Error: Common name cannot be specified with the -s flag", file=sys.stderr)
                sys.exit(1)
            elif key not in {
                'C',  'countryName',
                'L',  'localityName',
                      'emailAddress',
                'O',  'organizationName',
                'OU', 'organizationalUnitName',
                'ST', 'stateOrProvinceName'
                      'name',
                'SN', 'surname',
                'GN', 'givenName',
                      'initals'
                }:
                print('Error: Unknown key for subject "{}"'.format(key), file=sys.stderr)
                sys.exit(1)

            subject[key] = value
    
        elif ':' in fragment:
            # make sure its on the white list
            typ, _ = fragment.split(":", 1)
            if typ not in ('email', 'URI', 'DNS', 'RID', 'IP', 'dirname', 'othername'):
                print("Error: Unknown SAN type, must be one of email, URI, DNS, RID, IP, dirname or othername:", fragment, file=sys.stderr)
                sys.exit(1)
            vals.append(fragment)
        else:
            fragment = "DNS:" + fragment
            vals.append(fragment)

    san = ','.join(vals)
    if san:
        try:
            san_ext = X509Extension(b'subjectAltName', False, san.encode('ASCII'))
        except crypto.Error as err:
            if err.args[0][0][1] == 'v2i_GENERAL_NAME_ex':
                print("Error: Unknown SAN type in list (must be one of email, URI, DNS, RID, IP, dirname or othername):", san, file=sys.stderr)
                sys.exit(1)
            elif err.args[0][0][2] == 'invalid null value':
                print("Error: SAN value cannot be empty or unspecified", file=sys.stderr)
                sys.exit(1)
            else:
                raise
        extensions.append(san_ext)

    for ext in options.extension:
        try:
            key, val = ext.split("=", 1)
        except ValueError:
            print("Error: No value specified for extension (missing '='):", ext, file=sys.stderr)
            sys.exit(1)
            
        if key.startswith('critical,'):
            key = key[9:]
            critical = True
        else:
            critical = False
            
        try:
            ext = X509Extension(key.encode('ASCII'), critical, val.encode('ASCII'))
        except crypto.Error as err:
            if err.args[0][0][1] == 'DO_EXT_NCONF':
                print("Error: Unknown Extension name:", key, file=sys.stderr)
                sys.exit(1)
            elif err.args[0][0][1] == 'v2i_ASN1_BIT_STRING':
                print("Error: Unknown Value (case sensitive):", val, file=sys.stderr)
                sys.exit(1)
            elif err.args[0][0][2] in ('invalid null name', 'invalid null value'):
                print("Error: Value cannot be empty or unspecified: (key: {})".format(key), file=sys.stderr)
                sys.exit(1)
            else:
                raise
        extensions.append(ext)

    if options.prompt:
        for keys, prompt in (
                     (('C',  'countryName',),            "Country (eg AU): "),
                     (('L',  'localityName',),           "Locality/Town: "),
                     ((      'emailAddress',),           "Email Address: "),
                     (('O',  'organizationName',),       "Organization: "),
                     (('OU', 'organizationalUnitName',), "Organizationl Unit: "),
                     (('ST', 'stateOrProvinceName'),     "State: "),
                    ):
            if all(x not in subject for x in keys):
                log.debug("Prompting for %s", keys)
                val = input(prompt)
                if val:
                    log.debug('Valid Value received, setting: %s="%s"', keys[0], val)
                    subject[keys[0]] = val
        
    connect_string = 'sqlite:///{}'.format(options.file)
    engine = create_engine(connect_string, echo=DEBUG)
    conn = engine.connect()
    # no-op if data exists
    metadata.create_all(engine)
    
    db = Database(conn)

    command = getattr(options, 'command', None)
    sub_command = getattr(options, 'sub_command', None)

    ### Keys ###    
    if command == "keys":
        if options.key_id:
            key = db.keys[options.key_id]['raw']
            key = load_privatekey(FILETYPE_ASN1, key)
            output = dump_privatekey(FILETYPE_PEM, key)
            sys.stdout.write(output.decode('ASCII'))
        else:
            print("ID | Key Type | Creation Date | Hash | Certificates | Comment")
            print("---+----------+---------------+------+--------------+---------")
    
            for key in db.keys:
                print("{k.id} | {k.key_strength} {k.key_type} | {k.generated_date} | None | None | {k.comment}".format(k=key))
            
    ### Requests ###
    elif command == "req":
        if sub_command == "new":
            if options.cert:
                key_id = options.cert
            elif options.key:
                key_id = options.key
            else:
                key_typ = {'dsa': TYPE_DSA,
                           'rsa': TYPE_RSA,
                           }.get(options.type)
                key_id, key = generate_key(db, key_typ, options.bits, options.comment)
            
            id, request = generate_request(db, common_name, key_id, options.ca, subject, extensions, options.digest, options.comment)
            
            output = dump_certificate_request(FILETYPE_PEM, request)
            sys.stdout.write(output.decode('ASCII'))
        
        if sub_command == "sign":
            id, cert = sign_request(db, options.req, options.ca)

            output = dump_certificate(FILETYPE_PEM, cert)
            sys.stdout.write(output.decode('ASCII'))
            
        else:
            if options.req_id:
                request = db.requests[options.req_id]['raw']
                request = load_certificate_request(FILETYPE_ASN1, request)
                output = dump_certificate_request(FILETYPE_PEM, request)
                sys.stdout.write(output.decode('ASCII'))
            else:
                print("ID | Name | Cert | Key | Comment")
                print("-" * 30)
                for req in db.requests:
                    print("{c.id} | {c.common_name} | {c.certificate} | {c.private_key} | {c.comment}".format(c=req))

    ### Certificates ###
    elif command == "cert":
        if sub_command == "new":
            if options.cert:
                key_id = options.cert
            elif options.key:
                key_id = options.key
            else:
                key_typ = {'dsa': TYPE_DSA,
                           'rsa': TYPE_RSA,
                           }.get(options.type)
                key_id, key = generate_key(db, key_typ, options.bits, options.comment)
            
            id, request = generate_certificate(db, common_name, key_id, options.ca, subject, extensions, options.digest, options.comment, 
                                            options.parent, options.days)
            
            output = dump_certificate(FILETYPE_PEM, request)
            sys.stdout.write(output.decode('ASCII'))

        else:
            if options.cert_id:
                cert = db.certs[options.cert_id]['raw']
                cert = load_certificate(FILETYPE_ASN1, cert)
                output = dump_certificate(FILETYPE_PEM, cert)
                sys.stdout.write(output.decode('ASCII'))
            else:
                # list
                if options.ca:
                    certs = list_cert_authorities(db._conn)
                else:
                    certs = db.certs
                
                print("{:<6} | {:<5} | {:<20} | {:<10} | {:<10}".format('ID', 'ca', 'name', 'lifetime', 'comment'))
                print("-" * ((6+5+20+10+10) + (3*4)))
                for cert in certs:
                    if options.human:
                        before = humanize.naturaltime(cert.valid_before)
                        after = humanize.naturaltime(cert.valid_after, future=True)
                    else:
                        before = cert.valid_before
                        after =  cert.valid_after
                    period = "{} to {}".format(after, before)
                    print("{c.id:<6} | {c.ca:<5} | {c.common_name:<20} | {period} | {c.comment}".format(c=cert, period=period))
    else:
        args.print_usage()
        sys.exit(1)
    
    sys.exit(0)
           

if __name__ == "__main__":
    main()
