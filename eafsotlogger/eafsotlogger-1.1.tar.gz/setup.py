
#from distutils.core import setup
import os
import sys
from setuptools import setup, Extension

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = ["things/*"]

setup(name = "eafsotlogger",
    version = "1.1",
    description = "SOT Library, Maintain log in casandra database using python script.",
    author = "Raj",
    author_email = "raj.pawar@netcore.co.in",
    url = "http://www.netcore.in/",
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found 
    #recursively.)
    packages = ['soteventlogger'],
    #'package' package must contain files (see list above)
    #I called the package 'package' thus cleverly confusing the whole issue...
    #This dict maps the package name =to=> directories
    #It says, package *needs* these files.
    package_data = {'package' : files },
    #'runner' is in the root.
    scripts = ["runner"],
    long_description = """SOT Library. Maintain all events log in database.""",
    install_requires=[
        "cassandra-driver",
    ],
    #
    #This next part it for the Cheese Shop, look a little down the page.
    classifiers=[      
      'Development Status :: 4 - Beta',
      'Environment :: X11 Applications :: GTK',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python',
      'Topic :: Desktop Environment',
      'Topic :: Text Processing :: Fonts'
   ],
) 
