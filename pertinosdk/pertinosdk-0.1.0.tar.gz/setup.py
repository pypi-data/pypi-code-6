'''
Created on Jul 25, 2014

@author: lwoydziak
'''
from setuptools import setup
import glob
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


#scripts = glob.glob("application/*")

setup(name='pertinosdk',
      version='0.1.0',
      maintainer='Pertino Inc.',
      maintainer_email='developer@pertino.com',
      url = 'https://github.com/Pertino/pertino-sdk-python',
      download_url = 'https://github.com/Pertino/pertino-sdk-python/tarball/0.1',
      platforms = ["any"],
      description = 'Python package for communicating with Pertino.',
      long_description = read('README.rst'),
      classifiers = [
            'Development Status :: 3 - Alpha',
            'Natural Language :: English',
            'Operating System :: Unix',
            'Programming Language :: Python',
            'Programming Language :: Unix Shell',
            'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      packages=[
                'pertinosdk'
               ],
      install_requires=[
                         "requests"
                        ],
      keywords = ['pertino', 'sdk', 'api'],
      license='LICENSE.txt'
#       scripts=scripts
      )

