from setuptools import setup, find_packages
import sys, os

import jenkinsyamlconfigs

kw = {}
if sys.version_info >= (3,):
    kw['use_2to3'] = True

setup(name='jenkinsyamlconfigs',
      version=jenkinsyamlconfigs.__version__,
      author=jenkinsyamlconfigs.__author__,
      author_email=jenkinsyamlconfigs.__author_email__,
      url=jenkinsyamlconfigs.__url__,
      description=jenkinsyamlconfigs.__description__,
      long_description=open('README.md').read(),
      license=open('LICENSE').read(),
      install_requires=open('requirements.txt').read().splitlines(),
      tests_require=open('test_requirements.txt').read().splitlines(),
      setup_requires=[],      
      keywords='',
      packages=find_packages(),
      package_data = {'': ['*.xml','*.yml', '*.sh']},
      namespace_packages=[],
      zip_safe=False,
      test_suite='nose.collector',
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3',
                   'Topic :: Software Development :: Testing',
                   ],
      **kw)
