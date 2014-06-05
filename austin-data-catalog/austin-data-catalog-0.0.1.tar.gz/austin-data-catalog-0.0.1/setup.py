from distutils.core import setup

setup(name='austin-data-catalog',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Archive the /api/views endpoint on Austin\'s data catalog.',
      url='https://github.com/tlevine/austin-data-catalog',
      packages=[],
      install_requires = [
          'pluplusch>=0.0.7',
      ],
      scripts = ['austin'],
      version='0.0.1',
      license='AGPL',
)
