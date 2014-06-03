'''
Created on May 31, 2014

@author: minjoon
'''

from distutils.core import setup

setup(
      name='tinyocr',
      version='0.2.3',
      author='Min Joon Seo',
      author_email='minjoon@cs.washington.edu',
      packages=['tinyocr', 'tinyocr.test', 'tinyocr.feature', 'tinyocr.learner', 'tinyocr.const'],
      scripts=[],
      url='http://pypi.python.org/pypi/tinyocr/',
      license='LICENSE.txt',
      description='Single Character OCR',
      long_description=open('README.txt').read(),
)
