from distutils.core import setup

from pluplusch.meta import __version__, __author__

setup(name='pluplusch',
      author=__author__,
      author_email='_@thomaslevine.com',
      description='Big dada: Download data from lots of open data platforms.',
      url='https://github.com/tlevine/pluplusch',
      packages=['pluplusch'],
      install_requires = [
          'thready>=0.1.4',
          'picklecache>=0.0.3',
          'requests>=2.2.1',
          'pickle_warehouse>=0.0.17'
      ],
      scripts = ['bin/pluplusch'],
      tests_require = ['nose'],
      version=__version__,
      license='AGPL',
)
