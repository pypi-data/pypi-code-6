from setuptools import setup, find_packages

requires = [ "pyyaml>=3.10" ]

setup(name="finny",
      version="0.3.10",
      platforms='any',
      packages = find_packages(),
      include_package_data=True,
      install_requires=requires,
      author = "Bogdan Gaza",
      author_email = "bc.gaza@gmail.com",
      url = "https://github.com/hurrycane/finny",
      description = """Finny is the act of being skinny and fat at the same time.
                     Basic structure for an api-centry approach to Flask - that is both fat in skinny,
                     with basic and augmented support over some popular Flask libs""",
      entry_points = {'console_scripts': [ 'finny = finny.runner:execute_from_cli' ]},
      test_requirements = [],
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: System :: Networking',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
      ]
)
