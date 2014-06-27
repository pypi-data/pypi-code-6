from setuptools import setup, find_packages
from setuptools.command.install import install
import os


class MyCommand(install):
    """Dirty hack to install PyNaCl with pip as it doesn't work automatically
    on some machines."""

    def run(self):
        os.system("pip install PyNaCl")
        install.run(self)


setup(name='coinop',
      cmdclass={'install': MyCommand},
      version='0.0.2',
      description='Crypto-currency conveniences',
      url='http://github.com/BitVault/coinop-py',
      author='Matthew King',
      author_email='matthew@bitvault.io',
      license='MIT',
      packages=find_packages(exclude=[
          u'*.tests', u'*.tests.*', u'tests.*', u'tests']),
      install_requires=[
          'PyNaCl',
          'cffi',
          'pytest',
          'pycrypto',
          'python-bitcoinlib',
          'pycoin',
          'PyYAML',
          'ecdsa'
      ],
      zip_safe=False)
