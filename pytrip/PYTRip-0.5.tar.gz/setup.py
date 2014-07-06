from distutils.core import setup
setup(name='PYTRip',
      version='0.5',
      description='A collection of python functions to aid in ripping songs from YouTube',
      url='https://github.com/Rhysjc/PYTRip',
      author='Rhys Camm',
      author_email='rhysjc@gmail.com',
      py_modules=['PYTRip'],
      download_url='https://github.com/Rhysjc/PYTRip/tarball/0.5',
      install_requires=[
          'beautifulsoup4',
          'pafy',
          'phdub',
    ]
      )
