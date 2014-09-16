from setuptools import setup
from setuptools import find_packages


setup(
    name='PGeoTRMM',
    version='0.1.0',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pgeo',
        'flask'
    ],
    url='http://pypi.python.org/pypi/PGeoTRMM/',
    license='LICENSE.txt',
    description='TRMM plug-in for PGeo.',
    long_description=open('README.md').read()
)
