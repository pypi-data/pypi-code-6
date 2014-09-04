# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='validate-email-address',
      version='1',
      download_url='https://github.com/heropunch/validate-email-address.git',
      py_modules=('validate_email_address',),
      author='Carlos Killpack',
      author_email='carlos.killpack@rocketmail.com',
      description='Verify if an email address is valid and really exists.',
      long_description=open('README.rst').read(),
      keywords='email validation verification mx verify',
      url='http://github.com/heropunch/validate-email-address',
      license = 'LGPLv3',
      classifiers=('Topic :: Communications :: Email',
                   'Topic :: Utilities',
                   'License :: OSI Approved',
                   'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3', ))
