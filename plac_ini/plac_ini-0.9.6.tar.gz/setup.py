from setuptools import setup
import os.path

with open('README.txt') as f:
    long_desc = f.read()

setup(name='plac_ini',
      version='0.9.6',
      description=('Adds configuration file support to plac'),
      long_description=long_desc,
      author='Brent Woodruff',
      author_email='brent@fprimex.com',
      url='https://github.com/fprimex/plac_ini',
      license="BSD License",
      py_modules = ['plac_ini'],
      scripts = [],
      install_requires=['plac'],
      keywords="command line arguments ini file parser",
      platforms=["All"],
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Utilities'],
      zip_safe=False)

