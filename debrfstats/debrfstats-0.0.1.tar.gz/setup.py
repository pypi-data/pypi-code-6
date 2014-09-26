import os
import sys

try:
        from setuptools import setup
except ImportError:
        from distutils.core import setup


setup (
        name = "debrfstats",
        version = "0.0.1",
        description = "debrfstats is a library to generate Debian RFS statistics",
        long_description = open("README.md").read(),
        author = "Dariusz Dwornikowski", 
        author_email = "dariusz.dwornikowski@cs.put.poznan.pl",
        url = "https://github.com/tdi/debrfstats",
        packages = ["debrfstats" ],
        package_data={'': ['LICENCE']},
        requires = [
           'SOAPpy (>=0.12.0)',
           'dateutil (>=1.4)', 
           'requests (>=2.3.0)',
            ],
        install_requires = ['SOAPpy >= 0.12.0', 'dateutil >=1.4', 'requests>=2.3.0'],
        license = "GPL-3",
        zip_safe = False,

        classifiers = [
            'Environment :: Console',
            'Development Status :: 4 - Beta',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Operating System :: POSIX',
            ],
)



