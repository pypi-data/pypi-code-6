

from distutils.core import setup
from setuptools import setup
setup(name='NYPL',
      version='1.0.0',
      description='An unoffical API for the New York Public Library',
      author='Susan Steinman',
      author_email="steinman.tutoring@gmail.com"
      url='https://github.com/susinmotion/NYPL',
      packages=['NYPL'],
      packages_dir={'NYPL': 'NYPL'},
      install_requires=['requests', 'beautifulsoup4']
     )