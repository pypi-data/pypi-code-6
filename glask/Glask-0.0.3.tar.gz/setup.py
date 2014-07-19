from sys import argv

from setuptools import setup

version = '0.0.3'

install_requires = ['Flask>=0.10.1']
if 'develop' in argv[1:]:
    install_requires += ['pytest>=2.5.2']

setup(name='Glask', version=version, packages=['glask'], license='BSD',
      description='An extension for flask applications with best practices.',
      install_requires=install_requires)
