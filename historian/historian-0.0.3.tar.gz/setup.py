from distutils.core import setup

setup(name='historian',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Parse Tom\'s history files',
      url='http://small.dada.pink/historian',
      packages=['historian_reader'],
      tests_require = ['nose'],
      scripts = ['read-history'],
      version='0.0.3',
      license='AGPL',
)
