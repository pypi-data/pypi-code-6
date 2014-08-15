# -*- coding: utf-8 -*-
__revision__ = "$Id: $" # for the SVN Id
from setuptools import setup, find_packages

_MAJOR               = 0
_MINOR               = 9
_MICRO               = 1
version              = '%d.%d.%d' % (_MAJOR, _MINOR, _MICRO)
release              = '%d.%d' % (_MAJOR, _MINOR)

metainfo = {
    'authors': {"main": ("Thomas Cokelaer", "cokelaer@gmail.com")},
    'version': version,
    'license' : 'GPL',
    'download_url' : ['http://pypi.python.org/pypi/pypiview'],
    'url' : ["http://pythonhosted.org/pypiview/"],
    'description': "Utility to visualise the number of downloads of a package available on Pypi website" ,
    'platforms' : ['Linux', 'Unix', 'MacOsX', 'Windows'],
    'keywords' : [''],
    'classifiers' : [
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules'
          ]
    }



setup(
    name             = "pypiview",
    version          = version,
    maintainer       = metainfo['authors']['main'][0],
    maintainer_email = metainfo['authors']['main'][1],
    author           = metainfo['authors']['main'][0],
    author_email     = metainfo['authors']['main'][1],
    long_description = open("README.rst").read(),
    keywords         = metainfo['keywords'],
    description      = metainfo['description'],
    license          = metainfo['license'],
    platforms        = metainfo['platforms'],
    url              = metainfo['url'],
    download_url     = metainfo['download_url'],
    classifiers      = metainfo['classifiers'],

    # package installation
    package_dir = {'':'src'},
    #packages = ["pypiview"],

    install_requires = ['vanity', 'numpy', 'pandas', 'matplotlib'],

    #use_2to3 = True, # causes issue with nosetests


    entry_points = {
        'console_scripts': [
            'pypiview=pypiview:main',
            ]
        },



)
