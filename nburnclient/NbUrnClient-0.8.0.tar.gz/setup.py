from setuptools import setup, find_packages
from setuptools.command.install import install as InstallCommand

setup(
    name='NbUrnClient',
    version='0.8.0',
    author='Rune Lain Knudsen',
    author_email='rune.knudsen@uib.no',
    packages=find_packages(),
    url='https://github.com/runelk/NB_URN_Client_Python',
    license='LICENSE.txt',
    description='Python Client for the URN PID service at the National Library of Norway',
    long_description=open('README.rst').read(),
    install_requires=[
        'PyYAML',
        'suds==0.4'
    ]
)
