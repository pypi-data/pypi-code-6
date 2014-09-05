from distutils.core import setup
from distutils.sysconfig import get_python_lib
import os

setup(
	name='WestFax',
	version='0.1.2',
	author='Chris Brown',
	author_email='chris.brown@nwyc.com',
	packages=['westfax'],
	url='https://github.com/constituentvoice/WestFax',
	license='BSD',
	description='Python wrapper for the WestFax API',
	long_description=open('README.rst').read(),
	install_requires=['requests >= 1.0.0']
)
