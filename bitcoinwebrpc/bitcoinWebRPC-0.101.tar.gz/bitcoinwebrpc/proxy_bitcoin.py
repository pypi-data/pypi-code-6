# 2014 benjyz
# Copyright (C) 2007 Jan-Klaas Kollhof
# Copyright (C) 2011-2014 The python-bitcoinlib developers
#
# This file is part of python-bitcoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

"""Bitcoin RPC via HTTP"""

from __future__ import absolute_import, division, print_function, unicode_literals

try:
    import http.client as httplib
except ImportError:
    import httplib
import base64
import binascii
import decimal
import json
import os
import platform
import sys
try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

import bitcoin

USER_AGENT = "AuthServiceProxy/0.1"

HTTP_TIMEOUT = 30

unhexlify = binascii.unhexlify
hexlify = binascii.hexlify
if sys.version > '3':
    unhexlify = lambda h: binascii.unhexlify(h.encode('utf8'))
    hexlify = lambda b: binascii.hexlify(b).decode('utf8')


class JSONRPCException(Exception):
    def __init__(self, rpc_error):
        super(JSONRPCException, self).__init__('msg: %r  code: %r' %
                (rpc_error['message'], rpc_error['code']))
        self.error = rpc_error

class ProxyBitcoin(object):
    # FIXME: need a CChainParams rather than hard-coded service_port
    def __init__(self, service_url=None,
                       service_port=None,
                       btc_conf_file=None,
                       timeout=HTTP_TIMEOUT,
                       _connection=None):
        """Low-level JSON-RPC proxy

        Unlike Proxy no conversion is done from the raw JSON objects.
        """

        if service_url is None:
            # Figure out the path to the bitcoin.conf file
            if btc_conf_file is None:
                if platform.system() == 'Darwin':
                    btc_conf_file = os.path.expanduser('~/Library/Application Support/Bitcoin/')
                elif platform.system() == 'Windows':
                    btc_conf_file = os.path.join(os.environ['APPDATA'], 'Bitcoin')
                else:
                    btc_conf_file = os.path.expanduser('~/.bitcoin')
                btc_conf_file = os.path.join(btc_conf_file, 'bitcoin.conf')

            # Extract contents of bitcoin.conf to build service_url
            with open(btc_conf_file, 'r') as fd:
                conf = {}
                for line in fd.readlines():
                    if '#' in line:
                        line = line[:line.index('#')]
                    if '=' not in line:
                        continue
                    k, v = line.split('=', 1)
                    conf[k.strip()] = v.strip()

                if service_port is None:
                    service_port = bitcoin.params.RPC_PORT
                conf['rpcport'] = int(conf.get('rpcport', service_port))
                conf['rpcssl'] = conf.get('rpcssl', '0')

                if conf['rpcssl'].lower() in ('0', 'false'):
                    conf['rpcssl'] = False
                elif conf['rpcssl'].lower() in ('1', 'true'):
                    conf['rpcssl'] = True
                else:
                    raise ValueError('Unknown rpcssl value %r' % conf['rpcssl'])

                service_url = ('%s://%s:%s@localhost:%d' %
                    ('https' if conf['rpcssl'] else 'http',
                     conf['rpcuser'], conf['rpcpassword'],
                     conf['rpcport']))

        self.__service_url = service_url
        self.__url = urlparse.urlparse(service_url)
        if self.__url.port is None:
            port = 80
        else:
            port = self.__url.port
        self.__id_count = 0
        authpair = "%s:%s" % (self.__url.username, self.__url.password)
        authpair = authpair.encode('utf8')
        self.__auth_header = b"Basic " + base64.b64encode(authpair)

        if _connection:
            # Callables re-use the connection of the original proxy
            self.__conn = _connection
        elif self.__url.scheme == 'https':
            self.__conn = httplib.HTTPSConnection(self.__url.hostname, port=port,
                                                  key_file=None, cert_file=None,
                                                  timeout=timeout)
        else:
            self.__conn = httplib.HTTPConnection(self.__url.hostname, port=port,
                                                 timeout=timeout)


    def _call(self, service_name, *args):
        """make the HTTP call, always as POST
        RFC specs 
        http://tools.ietf.org/html/rfc2616
        http://tools.ietf.org/html/rfc4627
        """
        self.__id_count += 1

        postdata = json.dumps({'version': '1.1',
                               'method': service_name,
                               'params': args,
                               'id': self.__id_count})

        self.__conn.request('POST', self.__url.path, postdata,
                            {'Host': self.__url.hostname,
                             'User-Agent': USER_AGENT,
                             'Authorization': self.__auth_header,
                             'Content-type': 'application/json'})

        response = self._get_response()
        if response['error'] is not None:
            raise JSONRPCException(response['error'])
        elif 'result' not in response:
            raise JSONRPCException({
                'code': -343, 'message': 'missing JSON-RPC result'})
        else:
            return response['result']


    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            # Python internal stuff
            raise AttributeError

        # Create a callable to do the actual call
        f = lambda *args: self._call(name, *args)

        # Make debuggers show <function bitcoin.rpc.name> rather than <function
        # bitcoin.rpc.<lambda>>
        f.__name__ = name
        return f

    def _get_response(self):
        """get the HTTP response"""
        http_response = self.__conn.getresponse()
        if http_response is None:
            raise JSONRPCException({
                'code': -342, 'message': 'missing HTTP response from server'})

        return json.loads(http_response.read().decode('utf8'),
                          parse_float=decimal.Decimal)
