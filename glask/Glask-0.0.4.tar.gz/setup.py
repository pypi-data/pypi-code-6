from sys import argv

from setuptools import setup

version = '0.0.4'

install_requires = ['Flask>=0.10.1', 'python-dateutil>=2.2']
if 'develop' in argv[1:]:
    install_requires += ['pytest>=2.5.2']

setup(name='Glask', version=version, packages=['glask'], license='BSD',
      description='An extension for flask applications with best practices.',
      url='https://github.com/vamf12/Glask',
      install_requires=install_requires)
