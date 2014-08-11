#!/usr/bin/env python
 
import sys, os, platform
from distutils.core import setup
from distutils.command.sdist import sdist
from distutils.extension import Extension

cxx_compile_flags = []

def read(fname):
	return open(os.path.join('.', fname)).read()

def check_deps():
	if sys.version_info[:2] < (2,7):
		raise RuntimeError("This module has not been tested on versions of Python earlier than 2.7")
	if sys.version_info[:2] > (3,0):
		print "This module has not been tested on Python 3.x, it may/may not work"

def add_cxxflags():
	if sys.version.find('GCC') > 0:
		cxx_compile_flags.append('-std=c++11')
	
	if platform.python_compiler()[4:5] < '4'or platform.python_compiler()[6:7] < '6':
		raise RuntimeError("This module requires C++11 support with among other things "
							"nullptr support (GCC 4.6.x). Please upgrade GCC")

check_deps() 
add_cxxflags()

setup(	name='entDevType',
		version='0.1.1',
		description='A module for calculating the entropy/entropic deviations in data',
		long_description=read('README.txt'),
		author='Justin N. Ferguson',
		author_email='jf@ownco.net',
		url='https://github.com/jnferguson/entropyDeviation/',
		license='OSI Approved :: BSD License',
		platforms=[ 'POSIX', 'POSIX :: Linux' ], 
		classifiers=[
				'Development Status :: 2 - Pre-Alpha',
				'Environment :: Console',
				'Intended Audience :: Developers',
				'Intended Audience :: Science/Research',
				'Intended Audience :: System Administrators',
				'License :: OSI Approved :: BSD License',
				'Natural Language :: English',
				'Operating System :: POSIX',
				'Operating System :: POSIX :: Linux',
				'Programming Language :: C++',
				'Programming Language :: Python :: 2.7',
				'Topic :: Scientific/Engineering',
				'Topic :: Scientific/Engineering :: Information Analysis',
				'Topic :: Security',
				'Topic :: Security :: Cryptography',
				'Topic :: Utilities'
		],
	packages=['entropyDeviationType'],
    ext_modules=[
        Extension("entDevType", [
			'src/entropy.cpp',		  		'src/entropy_wrapper.cpp',   'src/xor_table.cpp',
			'src/entropy_deviation.cpp', 	'src/xor_table_wrapper.cpp', 
			# 'src/key_sizer_recover.cpp',
		],
		language='c++',
		extra_compile_args=cxx_compile_flags,
		libraries = ["boost_python"])
    ], 
	scripts=['bin/edfind.py'])
