
from setuptools import setup

setup(
  name = 'onetworedblue',
  packages = ['onetworedblue',],
  package_data={'': ['*.kv', '*.png', '*.ico']},
  version = '0.1.1',
  description = 'A tool for identifiying and counting benthic organisms in bottom photographs',
  author = 'Eric Gallimore',
  url="http://www.ericgallimore.com/projects/onetworedblue",
  author_email = 'fishrock@ericgallimore.com',
  keywords = ['onetworedblue', 'fishrock', 'fish_rock', 'photographs', 'benthic'],
  license='GPLv3+',
  classifiers = [],
  entry_points = {'console_scripts': ['onetworedblue = onetworedblue.main:run_application']},

  install_requires=[
        "cython",
        "kivy >= 1.8.0",
        "Pillow",
    ],
)