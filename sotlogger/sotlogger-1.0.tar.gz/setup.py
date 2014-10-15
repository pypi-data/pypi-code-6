import os
import sys
from setuptools import setup, Extension

#files = ["things/*"]
setup(name = "sotlogger",
    version = "1.0",
    description = "SOT Library, Maintain event logs in casandra database using python connection script.",
    author = "Raj",
    author_email = "raj.pawar@netcore.co.in",
    url = "http://www.netcore.in/",
    packages = ['soteventlogger'],
    #package_data = {'package' : files },
    scripts = ["runner"],
    long_description = """SOT Library. Maintain event logs in casandra database using python connection script.""",
    install_requires=[
        "cassandra-driver",
    ],
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