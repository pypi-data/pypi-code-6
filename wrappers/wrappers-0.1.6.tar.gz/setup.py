from setuptools import setup
from os.path import normpath, dirname, basename
from contextlib import contextmanager
import os, shutil, glob, sys, logging

logging.basicConfig(level=0)

log = logging.getLogger(sys.argv[0])

# setup.py: {CWD}/path/to/{project}/setup.py
# package directory: {CWD}/path/to/{project}/{package_dir}

# simple implementation of a directory stack
# http://stackoverflow.com/a/3012921/41957
@contextmanager
def dirstack(_path):
	old_path = os.getcwd()
	os.chdir(_path)
	yield
	os.chdir(old_path)

def detect_project_name():
	try:
	    log.debug(normpath(sys.argv[0]).split(os.sep))
	    name = normpath(sys.argv[0]).split(os.sep)[-2]
	except IndexError:
	    name = basename(os.path.abspath(os.getcwd()))

	# replace dash with underscore
	return name.replace('-', '_')

name = detect_project_name()
log.debug("project name = %s" %(name))

# Run in the same directory as the setup.py script
with dirstack(dirname(os.path.abspath(sys.argv[0]))):
	setup(name=name,
	      version='0.1.6',
			author='comsul',
			author_email='chnrxn+pypi@gmail.com',
			description="convenient wrappers around existing modules", 
	      packages=['wrappers'],
	      # modules=[], 
	      # install_requires=[]
	)
