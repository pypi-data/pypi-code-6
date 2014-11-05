#!/usr/bin/env 3python
# https://bitbucket.org/IntrepidusGroup/mallory/src/c13b232ef776b8ae206a58467a0eebd6babc225f/src/cert_auth.py
# http://docs.ganeti.org/ganeti/2.5/html/design-x509-ca.html
# http://www.openssl.org/docs/apps/x509v3_config.html

from OpenSSL.crypto import TYPE_RSA
import logging
import sys, os

__author__ = "Da_Blitz <code@blitz.works>"
__version__ = "0.1"
__email__ = "code@blitz.works"
__license__ = "BSD (3 Clause)"
__url__ = "http://blitz.works/blitz-ca"

log = logging.getLogger('blitz-ca')

DEFAULT_KEY_TYPE = TYPE_RSA
DEFAULT_KEY_SIZE = 2048
DEFAULT_DIGEST_TYPE = "sha256"
ENVIRON_DB = os.environ.get("BLITZ_CA_DATABASE")
HARDCODED_DB = os.path.expanduser("~/.blitz-ca.db")
DEFAULT_DB = ENVIRON_DB or HARDCODED_DB
