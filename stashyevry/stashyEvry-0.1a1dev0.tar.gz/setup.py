import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='stashyEvry',
      version="0.1a1dev0",
      description='Python API client for the Atlassian Stash REST API',
      long_description=read('README.rst'),
      url='http://github.com/RisingOak/stashy',
      download_url = 'https://github.com/RisingOak/stashy/tarball/0.1',
      author='Cosmin Stejerean',
      author_email='cosmin@offbytwo.com',
      license='Apache License 2.0',
      packages=['stashy', 'stashy.admin'],
      test_suite = 'tests',
      #scripts=['bin/stash'],
      #tests_require=open('test-requirements.txt').readlines(),
      install_requires=['decorator==3.4.0', 'requests==1.1.0'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries'
        ]
     )
