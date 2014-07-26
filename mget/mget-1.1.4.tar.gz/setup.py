#!/usr/bin/env python3 

__version__ = '1.1.4'

import glob
import os, warnings
from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext

base_path = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))

userconf = os.path.join(os.path.expanduser('~'), '.config')
cpy_src = os.path.join(os.path.expanduser('~'), base_path, './Mget/utils/cpysrc/')

ext_modules = [Extension( "mgetsys", [cpy_src + 'cpycode.pyx', cpy_src + 'mget.cpp'],
		extra_compile_args=["-std=c++11"], language="c++")]

files_spec = [	('share/doc/mget', ['README.txt']),
		('', glob.glob('*.so')),
		(userconf, ['mget.conf'])]
root = os.path.dirname(os.path.abspath(__file__))
data_files = []

for dirname, files in files_spec:
	resfiles = []
	for fn in files:
		if not os.path.exists(fn): warnings.warn('Skipping file %s.' % fn)
		else: resfiles.append(fn)
	data_files.append((dirname, resfiles))

params={'data_files': data_files,
	'entry_points': {'console_scripts': ['mget = Mget:main']}}
setup(
	name='mget',
	version=__version__,
	cmdclass = {'build_ext': build_ext},
	ext_modules = ext_modules,
	description='HTTP file/video downloader',
	long_description='Small command-line program to download videos from  mp4upload.com & video sharing site and other http urls.',
	author='Ramesh Mani Maran',
	author_email='r4v0n3@gmail.com',
	packages=find_packages(),
	classifiers=[
	"Development Status :: 5 - Production/Stable",
	"Environment :: Console",
	"License :: Public Domain",
	"Operating System :: POSIX :: Linux",
	"Topic :: Internet",
	"Programming Language :: Python :: 3.4",
	],
	keywords='download mget http file downloader video mp4upload',
	**params)

