#!/usr/local/bin/python

""" Configuration for the eGenix web installer test package.

    Copyright (c) 2014, eGenix.com Software GmbH; mailto:info@egenix.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.
"""
import sys, os
from mxSetup import mx_Extension, mx_version

#
# Package version
#
version = mx_version(0, 2, 0)

#
# Setup information
#
name = "egenix-web-installer-test"

#
# Meta-Data
#
description = "eGenix Web Installer Test Package "
long_description = """\
This is a test package for the eGenix Web Installer that comes with
the latest mxSetup.

The test package will install mxDateTime using a package which
dynamically downloads and runs a precompiled binary package for
the installation platform. It also supports fallback to the source
package and compilation using a compiler, in case no suitable
binary package can be found.

The test package should be compatible with:

* Python 2.5 - 2.7

* easy_install, pip and zc.buildout

* manual "python setup.py install"

More documentation will follow as we make progress with the
web installer.

This software is brought to you by eGenix.com and distributed under
the eGenix.com Public License 1.1.0.
"""
license = (
"eGenix.com Public License 1.1.0; "
"Copyright (c) 2014, eGenix.com Software GmbH, All Rights Reserved"
)
author = "eGenix.com Software GmbH"
author_email = "info@egenix.com"
maintainer = "eGenix.com Software GmbH"
maintainer_email = "info@egenix.com"
url = "http://www.egenix.com/"
download_url = url
platforms = [
    'Windows',
    'Linux',
    'FreeBSD',
    #'Solaris',
    'Mac OS X',
    #'AIX',
    ]
classifiers = [
    "Environment :: Console",
    "Environment :: No Input/Output (Daemon)",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Python License (CNRI Python License)",
    "License :: Freely Distributable",
    "License :: Other/Proprietary License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Operating System :: MacOS",
    "Operating System :: Other OS",
    "Programming Language :: C",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.4",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities ",
    ]
if 'a' in version:
    classifiers.append("Development Status :: 3 - Alpha")
elif 1 or 'b' in version:
    classifiers.append("Development Status :: 4 - Beta")
else:
    classifiers.append("Development Status :: 5 - Production/Stable")
    classifiers.append("Development Status :: 6 - Mature")
classifiers.sort()

#
# Python packages
#
packages = [

    # mx Extensions Base Package
    'mx',

    # mxDateTime (to have an example)
    'mx.DateTime',
    'mx.DateTime.mxDateTime',
    'mx.DateTime.Examples',

    # Misc. other modules
    'mx.Misc',

    ]

#
# C Extensions
#

# Determine optional platform-dependent features
if sys.platform[:3] != 'win':
    # Unix-like platforms
    _mxDateTime_optional_libraries = [
        # mxDateTime needs floor() and ceil() which are sometimes
        # defined in libm. Python normally already references this
        # library if necessary, so not finding the library is not
        # necessarily a reason to fail building mxDateTime.
        ('m', ['math.h']),
        # mxDateTime can use the API clock_gettime() if available,
        # but this sometimes needs the librt to be available.
        ('rt', ['time.h']),
        ]
else:
    # On Windows, the extra libs are not needed (or even available)
    _mxDateTime_optional_libraries = []
    
# Extension definitions
ext_modules = [

    # mxDateTime
    mx_Extension('mx.DateTime.mxDateTime.mxDateTime',
                 ['mx/DateTime/mxDateTime/mxDateTime.c'],
                 # If mxDateTime doesn't compile, try removing the next line.
                 define_macros=[('USE_FAST_GETCURRENTTIME', None)],
                 #
                 include_dirs=['mx/DateTime/mxDateTime'],
                 optional_libraries=_mxDateTime_optional_libraries,
                 ),

    ]

#
# Data files
#
data_files = [

    # Copyright, licenses, READMEs
    'mx/COPYRIGHT',
    'mx/LICENSE',
    'mx/README',

    # mxDateTime
    'mx/DateTime/Doc/mxDateTime.pdf',
    'mx/DateTime/COPYRIGHT',
    'mx/DateTime/LICENSE',
    'mx/DateTime/README',
    'mx/DateTime/mxDateTime/mxDateTime.h',
    'mx/DateTime/mxDateTime/mxh.h',

    ]

#
# Dependencies
#
if sys.version[:3] >= '2.5':
    # Required other packages; Note: the package name has to be given
    # using underscores, since setuptools doesn't like hyphens in
    # package names.
    requires = [
        #'egenix_mx_base',
        ]

#
# Declare namespace packages (for building eggs)
#
namespace_packages = [
    'mx',
    ]
