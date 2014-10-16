

from distutils.core import setup
from setuptools import setup
with open('NYPL/README.md') as file:
    long_description = file.read()
setup(name='NYPL',
      version='0.1.2',
      description='An unoffical API for the New York Public Library',
      author='Susan Steinman',
      author_email="steinman.tutoring@gmail.com",
      url='https://github.com/susinmotion/NYPL',
      packages=['NYPL'],
      long_description=long_description,
      install_requires=['requests>=1.2.0', 'beautifulsoup4']
     )