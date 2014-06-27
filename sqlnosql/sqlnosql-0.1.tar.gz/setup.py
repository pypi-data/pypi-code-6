import os
from setuptools import setup, find_packages
version = '0.1'
README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(README).read()
setup(name='sqlnosql',
      version=version,
      description=("Push semi-structured data (e.g. JSON documents) into a database with a minimum of fuss. Includes validation and schema migration."),
      long_description=long_description,
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'
                    ],
      install_requires=[
            'sqlalchemy>=0.9', 
            'csvkit>=0.7', 
            'jsonschema>=2.3', 
            'docopt>=0.6', 
      ], 
      keywords='etl sql nosql postgres migrations transform load extract',
      author='Stijn Debrouwere',
      author_email='stijn@stdout.be',
      download_url='http://www.github.com/newslynx/nosqlsql/tarball/master',
      license='MIT',
      test_suite='sqlnosql.tests',
      packages=find_packages(),
      )