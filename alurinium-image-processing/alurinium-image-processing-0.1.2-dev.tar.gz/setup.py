from setuptools import setup, find_packages

setup(
    name='alurinium-image-processing',
    version='0.1.2-dev',
    author='Vasiliy Sheredeko',
    author_email='piphon@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/alurinium-image-processing/',
    license='LICENSE.txt',
    description='Useful image processing utils using Pillow',
    long_description=open('README.md').read(),
    install_requires=[
        "Pillow >= 2.3.0",
        'six >= 1.7.3'
    ],
)