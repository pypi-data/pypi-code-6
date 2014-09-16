from setuptools import setup
from setuptools import find_packages


setup(
    name='PGeoMODIS',
    version='0.1.4',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    install_requires=[
        'flask'
    ],
    url='http://pypi.python.org/pypi/PGeoMODIS/',
    license='LICENSE.txt',
    description='MODIS plug-in for PGeo.',
    long_description=open('README.md').read()
)
