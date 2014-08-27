import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

requires = [
    'specloud==0.4.5',
    'Shapely==1.2.14',
]

setup(name='ogr_utils',
      version='1.2',
      description='conveniance utilities for ogr',
      long_description=README,
      classifiers=["Programming Language :: Python :: 2.7", "Topic :: Scientific/Engineering :: GIS"],
      author="Lars Claussen, Thijs Creemers",
      author_email='lars.claussen@and.com',
      url='http://www.and.com/',
      keywords='org utility',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="ogr_utils",
      entry_points="""\
      """,
      )
