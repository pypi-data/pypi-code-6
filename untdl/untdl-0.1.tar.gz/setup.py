#!/usr/bin/env python

try:
    # use setuptools or distribute if available
    from setuptools import setup
except ImportError:
    from distutils.core import setup

base_version = '1.1.6r81'  # base version
fork_version = '0.1'

def get_version():
    """Probably a much more elegant way to do this.

    Update untdl/VERSION.txt with the current svn version, then return the result"""

    version = base_version + '-' + fork_version

    file = open('untdl/VERSION.txt', 'w')
    file.write(version)
    file.close()
    print('revision %s' % fork_version)

    return fork_version

setup(name='untdl',
      version=get_version(),
      author='Lee Cannon',
      author_email='leecannon.siy@gmail.com',
      description='Fork of tdl (Pythonic port of rogue-like library libtcod).',
      long_description=open('README.md', 'r').read(),
      url="https://github.com/leecannon/untdl",
      download_url="https://github.com/leecannon/untdl",
      packages=['untdl'],
      package_data={'untdl': ['*.txt', 'lib/*.txt', '*.bmp', '*.png', 'lib/win32/*',
                            'lib/darwin/*.dylib', 'lib/linux*/*']},
      install_requires=['ctypes'],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Win32 (MS Windows)',
                   'Environment :: MacOS X',
                   'Environment :: X11 Applications',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Operating System :: POSIX',
                   'Operating System :: MacOS',
                   'Operating System :: Microsoft :: Windows',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.0',
                   'Programming Language :: Python :: 3.1',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: Implementation :: CPython',
                   'Programming Language :: Python :: Implementation :: PyPy',
                   'Topic :: Games/Entertainment',
                   'Topic :: Multimedia :: Graphics',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
      keywords = 'portable rogue-like rogue-likes text ctypes ASCII ANSI Unicode libtcod fov',
      platforms = ['Windows', 'Mac OS X', 'Linux'],
      license = 'New BSD License'
      )
