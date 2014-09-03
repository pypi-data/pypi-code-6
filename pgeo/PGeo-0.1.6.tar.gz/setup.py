from setuptools import setup
from setuptools import find_packages
from setuptools import findall

setup(
    name='PGeo',
    version='0.1.6',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    install_requires=['GDAL'],
    package_data={
        'data_providers': [findall('config/data_providers')],
    },
    url='http://pypi.python.org/pypi/PGeo/',
    license='LICENSE.txt',
    description='PGeo module.',
    long_description=open('README.md').read()
)
