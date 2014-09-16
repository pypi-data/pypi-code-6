from setuptools import setup
from setuptools import find_packages


setup(
    name='PGeoMODIS',
    version='0.1.0',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pgeo',
        'flask'
    ],
    url='http://pypi.python.org/pypi/PGeoMODIS/',
    license='LICENSE.txt',
    description='PGeo module.',
    long_description=open('README.md').read()
)
