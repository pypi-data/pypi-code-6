from setuptools import setup
from setuptools import find_packages

setup(
    name='PGeo',
    version='0.1.8',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    install_requires=['GDAL'],
    url='http://pypi.python.org/pypi/PGeo/',
    license='LICENSE.txt',
    description='PGeo module.',
    long_description=open('README.md').read()
)
