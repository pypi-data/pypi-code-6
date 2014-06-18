from distutils.core import setup

setup(name='wbcontractawards',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Get information about World Bank contract awards',
      url='https://github.com/tlevine/wbcontractawards',
      packages=['wbcontractawards'],
      install_requires = ['lxml','picklecache','requests'],
      tests_require = ['nose'],
      scripts = ['bin/wbcontractawards'],
      version='0.0.3',
      license='AGPL',
)
