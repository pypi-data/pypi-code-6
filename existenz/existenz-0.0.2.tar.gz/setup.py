"""The setuptools setup file."""
from setuptools import setup

with open('README.txt') as file:
    long_description = file.read()

setup(
    name='existenz',
    version='0.0.2',
    author='Raul Gonzalez',
    author_email='mindbender@gmail.com',
    url='https://github.com/neoinsanity/existenz',
    license='Apache License 2.0',
    description='an existing individual',
    long_description=long_description,
    packages=['existenz', ],
    install_requires=[
        'cognate==0.0.1',
        'decorator==3.4.0',
    ],
    include_package_data=True,
)
