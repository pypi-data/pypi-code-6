#!/usr/bin/env python
#
# Copyright (C) 2014 Eric Welton
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose with or without fee is hereby granted,
# provided that the above copyright notice and this permission notice
# appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND HYPERDNS DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL HYPERDNS BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
import os
def purepath(rp):
    return os.path.join(os.path.dirname(__file__),rp)

# extract the version from the local file version.txt
version = 'unknown'
with open(purepath('version.txt')) as file:
    version=file.read()
version=version.strip()

# what is our documentation location
github = 'http://hyperdns.github.io/hapi-vendor-ultra'

from distutils.core import setup
from pip.req import parse_requirements

# parse_requirements() returns generator of
# pip.req.InstallRequirement objects
install_reqs = parse_requirements(purepath("requirements.txt"))
test_reqs = parse_requirements(purepath("dev-requirements.txt"))

# from: https://coderwall.com/p/qawuyq
# allows use of Markdown on GitHub and RST on PyPI
try:
   import pypandoc
   description = pypandoc.convert(purepath('README.md'), 'rst')
except (IOError, ImportError):
   description = 'Please consult %s' % github

kwargs = {
    'name' : 'hapi-vendor-ultra',
    'description' : 'Neustar UltraDNS Adapter for HyperDNS HAPI',
    'namespace_packages' : ['hyperdns','hyperdns.vendor','hyperdns.vendor.drivers'],
    'packages' : ['hyperdns.vendor.drivers.ultra'],
    'scripts':[],
    'version' : version,
    'long_description' : description,
    'author' : 'Eric Welton',
    'author_email' : 'eric@dnsmaster.io',
    'license' : 'BSD-like',
    'url' : github,
    'install_requires':[str(ir.req) for ir in install_reqs],
    'tests_require':[str(ir.req) for ir in test_reqs],
    'classifiers' : [
        "Programming Language :: Python",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]
    }
    
setup(**kwargs)
