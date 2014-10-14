# -*- coding: utf-8 -*-
"""
This module contains the tool of Products.mediaLink
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.0.1'

long_description = (
    read('docs/HISTORY.txt')
    )

tests_require = ['zope.testing']

setup(name='Products.mediaLink',
      version=version,
      description="Folderish Link",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='plone type link folderish',
      author='David Jonas, Andre Goncalves',
      author_email='david@itsnotthatkind.org, andre@intk.com',
      url='https://github.com/intk/Products.mediaLink',
      download_url="https://github.com/intk/Products.mediaLink/tarball/0.5",
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='Products.mediaLink.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
