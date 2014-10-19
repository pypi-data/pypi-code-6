from distutils.core import setup
from setuptools import find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='fabric-utils',
    version='0.0.3',
    keywords='fabric django apache',
    author='David Saenz Tagarro',
    author_email='david.saenz.tagarro@gmail.com',
    packages=find_packages(),
    url='https://github.com/dsaenztagarro/fabric-utils',
    license='LICENSE.txt',
    description='Fabric utils for deployment management',
    long_description=long_description,
)
