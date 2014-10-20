#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys,os,shutil

if sys.version_info.major==2:
	other_version = 3
else:
	other_version = 2

readme = changes = ''
if os.path.exists('README.rst'):
	readme = open('README.rst').read()
if os.path.exists('CHANGES.rst'):
	changes = open('CHANGES.rst').read()

install_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(install_dir,'scripts')
shutil.rmtree(scripts_dir,ignore_errors=True)
if not os.path.exists(scripts_dir):
	os.makedirs(scripts_dir)

pysite_command = 'pysite-%d.%d%s' % (sys.version_info.major,sys.version_info.minor,'.py' if sys.platform.find('win')==0 else '')
scriptfiles = [os.path.join('scripts',pysite_command)]
f_pysite_temp = open(os.path.join(install_dir,'script','templates','pysite'))
f_pysite_cmd = open(os.path.join(scripts_dir,pysite_command),'w')
f_pysite_cmd.write(f_pysite_temp.read().replace('<INTERPRETER>',sys.executable))
f_pysite_cmd.close()
f_pysite_temp.close()

if sys.platform.find('win')==0:
	pysite_bat = 'pysite-%d.%d.bat' % (sys.version_info.major,sys.version_info.minor)
	f_pysite_bat_temp = open(os.path.join(install_dir,'script','templates','pysite.bat'))
	data = f_pysite_bat_temp.read()
	f_pysite_bat_temp.close()
	data = data.replace('<INTERPRETER>',sys.executable)
	data = data.replace('<VERSION_MAJOR>',str(sys.version_info.major))
	data = data.replace('<VERSION_MINOR>',str(sys.version_info.minor))
	f_pysite_bat = open(os.path.join(scripts_dir,pysite_bat),'w')
	f_pysite_bat.write(data)
	f_pysite_bat.close()

VERSION = '0.2.4'

SHORT_DESC = "Create simple yet powerful WSGI based sites, utilizing Jinja2 and Qt's TS-file format for localization"

def walk_dir(dirname):
	files = []
	def detect_svn(fname):
		return fname.find('.svn')==-1
	for f in filter(detect_svn ,map(lambda fname: os.path.join(dirname,fname),os.listdir(dirname))):
		files += [f]
	return files

def packages(basedir):
	p = []
	for base,dirs,files in os.walk(basedir):
		if base.find('.svn')==-1:
			p+=['.'.join(base.split(os.path.sep)[1:])]
	return p

data_files= [
	(os.path.join('script','templates'),walk_dir(os.path.join('script/templates'))),
	(os.path.join('resources','init','static','css'),walk_dir(os.path.join('resources','init','static','css'))),
	(os.path.join('resources','init','static','images'),walk_dir(os.path.join('resources','init','static','images'))),
	(os.path.join('resources','init','static','lib'),walk_dir(os.path.join('resources','init','static','lib'))),
	(os.path.join('resources','init','templates'),walk_dir(os.path.join('resources','init','templates')))]


sinst = setup(
	name='pysite',
	packages=packages(os.path.join('src','pysite')),
	package_dir={'':'src'},
	version=VERSION,
	description=SHORT_DESC,
	long_description='\n\n'.join([readme, changes]),
	classifiers=[
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Operating System :: OS Independent',
		'Natural Language :: English',
		'Intended Audience :: Developers',
		'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',       
	],
	keywords= ['wsgi', 'website', 'www', 'website', 'framework'],
	author='Jakob Simon-Gaarde',
	author_email='jakob@simon-gaarde.dk',
	maintainer = 'Jakob Simon-Gaarde',
	maintainer_email = 'jakob@simon-gaarde.dk',
	install_requires=['jinja2','slimit'],
	requires=['jinja2','slimit'],
	provides=['pysite'],
	license='LGPL3',
	scripts=scriptfiles,
	data_files=data_files,
	zip_safe=False
)

