from setuptools import setup
from setuptools import find_packages

setup(
    name='PGeoREST',
    version='0.1.10',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/PGeoREST/',
    license='LICENSE.txt',
    description='PGeoREST module.',
    long_description=open('README.txt').read(),
    install_requires=[
        'flask',
        'flask-cors',
        'pgeo'
    ]
)
