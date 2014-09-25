# from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='ncdr',
    version='0.0.4',
    packages=find_packages(),
    license='',
    long_description=open('README.txt').read(),
    url='http://www.stoneworksolutions.net',
    author='StoneworkSolutions',
    author_email='desarrollo@stoneworksolutions.net',
    package_data={'': ['*.html']},
    include_package_data=True,
    install_requires=[],
    )
