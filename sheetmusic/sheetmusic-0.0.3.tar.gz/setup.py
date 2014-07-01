from distutils.core import setup

setup(name='sheetmusic',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Functions to be loaded by the Gnumeric Sheetmusic plugin',
      url='https://github.com/tlevine/sheetmusic',
      packages=['sheetmusic', 'libsheetmusic'],
      scripts=['bin/sheetmusic-installer'],
      install_requires = ['mingus', 'lxml'],
      tests_require = ['nose'],
      version='0.0.3',
      license='AGPL',
)
