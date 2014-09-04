from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup


setup(
    name='openjub_py',
    version='0.1',
    author='Tom Wiesing',
    author_email='tkw01536@gmail.com',
    packages=['openjub_py'],
    url='https://github.com/tkw1536/openjub_py',
    license='See LICENSE.txt',#
    install_requires=['requests'],
    description='A Python Client for OpenJUB. ',
    long_description=open('README.txt').read(),
)
