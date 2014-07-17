# encoding: utf-8

from setuptools import setup

try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    description = open("README.md", "rb").read()

setup(name='dwdweather',
      version='0.1',
      description='Inofficial DWD weather data client (Deutscher Wetterdienst)',
      long_description=description,
      author='Marian Steinbach',
      author_email='marian@sendung.de',
      url='http://github.com/marians/dwd-weather',
      py_modules=['dwdweather'],
      install_requires=[]
)
