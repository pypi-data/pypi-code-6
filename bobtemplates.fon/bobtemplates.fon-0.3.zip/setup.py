from setuptools import setup
from setuptools import find_packages
import os

version = '0.3'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = \
    read('README.rst') + \
    read('docs', 'CONTRIBUTORS.rst') + \
    read('docs', 'CHANGES.rst') + \
    read('docs', 'LICENSE.rst')

setup(name='bobtemplates.fon',
      version=version,
      description="Templates for fon projects",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Web Python Zope Plone Templates mr.bob',
      author='Franck NGAHA',
      author_email='franck.o.ngaha@gmail.com',
      url='https://github.com/fngaha/bobtemplates.fon',
      license='GPL V2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['bobtemplates'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'mr.bob',
          'ipdb',
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': [
            'coverage',
            'nose',
            'nose-selecttests',
            'scripttest',
            'unittest2',
           ],
      },
      entry_points={},
      )
