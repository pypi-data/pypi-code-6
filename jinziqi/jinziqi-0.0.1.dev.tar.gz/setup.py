#coding:utf-8
from setuptools import setup, find_packages

setup(name='jinziqi',
      version=':versiontools:jinziqi:',
      description="jinziqi for python",
      long_description="""""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      author='samleung',
      author_email='callsamleung@gmail.com',
      url='https://github.com/callsamleung/jinziqi_python',
      license='mit',
      packages=find_packages(exclude=['.git*']),
      zip_safe=False,
      setup_requires=[
          'versiontools>=1.8',
          ],
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      )
