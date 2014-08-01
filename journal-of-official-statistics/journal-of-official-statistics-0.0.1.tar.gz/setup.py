from distutils.core import setup

setup(name='journal-of-official-statistics',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Download articles from the Journal of Official Statistics',
      url='https://github.com/tlevine/jor',
      packages=['jos'],
      install_requires = ['picklecache','requests','lxml'],
     #tests_require = ['nose'],
      scripts = ['bin/jos'],
      version='0.0.1',
      license='AGPL',
)
