from distutils.core import setup

setup(name='commasearch',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Search for data tables.',
      url='https://github.com/tlevine/commasearch',
      packages=['commasearch'],
      install_requires = [
          'special_snowflake >= 0.0.8',
          'pickle_warehouse >= 0.0.18',
          'requests>=2.2.1',
          'thready>=0.1.3',
      ],
      scripts = [
          'bin/,',
      ],
      tests_require = ['nose'],
      version='0.0.3',
      license='AGPL',
      classifiers=[
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
)
