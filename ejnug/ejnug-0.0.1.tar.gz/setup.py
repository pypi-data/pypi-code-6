import os
from distutils.core import setup

setup(name = 'ejnug',
      author = 'Thomas Levine',
      author_email = '_@thomaslevine.com',
      description = 'Share emails publically',
      url = 'http://mail.thomaslevine.com',
      install_requires = [
          'lxml>=3.3.5',
          'bottle>=0.12.7',
          'notmuch>=0.15.2',
          'Unidecode>=0.04.16',
          'CherryPy>=3.6.0',
      ],
      tests_require = ['nose'],
      packages = ['ejnug'],
      scripts = [os.path.join('bin','ejnug')],
      version = '0.0.1',
      license = 'AGPL',
      include_package_data = True,
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
      ],
)
