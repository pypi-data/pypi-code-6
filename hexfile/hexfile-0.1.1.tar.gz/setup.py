import hexfile

try:
    from setuptools import setup, Command
except:
    from distutils.core import setup, Command

setup(name='hexfile',
      version=hexfile.__version__,
      packages=['hexfile'],
      description='Library for loading and manipulating hex files.',
      author='Ryan Sturmer',
      author_email='ryansturmer@gmail.com',
      url='http://www.github.com/ryansturmer/hexfile')
