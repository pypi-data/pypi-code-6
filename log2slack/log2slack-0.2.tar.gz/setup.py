from distutils.core import setup

from os import path

README = path.abspath(path.join(path.dirname(__file__), 'README.md'))

setup(
      name='log2slack',
      version='0.2',
      packages=['log2slack'],
      description='Simple logger for posting log to slack.com',
      long_description=open(README).read(),
      author='Rick Mak',
      author_email='rick.mak@gmail.com',
      url='https://github.com/rickmak/log2slack',
      license='MIT',
      requires=['requests']
)