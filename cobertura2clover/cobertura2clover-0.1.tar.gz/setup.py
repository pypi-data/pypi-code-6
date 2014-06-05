import os

from setuptools import setup, find_packages

requires = [
    'beautifulsoup4',
    'lxml'
]

setup(name='cobertura2clover',
      version='0.1',
      description='cobertura2clover',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      install_requires = requires,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      
      entry_points="""\
      [console_scripts]
      cobertura2clover = cobertura2clover.parser:main
      """
      )
