'''
Created on 30 Jun 2014

@author: julianporter
'''

from setuptools import setup, Extension
import os,os.path,re

allFiles=[]
for dir,_,files in os.walk('src'):
    allFiles.extend([os.path.join(dir,file) for file in files if file!='main.cpp' and file[-4:]=='.cpp'])        



homeDir='src'

module1 = Extension('pollinotify',
                    define_macros = [('MAJOR_VERSION', '0'),
                                     ('MINOR_VERSION', '1')],
                    include_dirs = ['/usr/local/include','/usr/include','src'],
                    libraries = ['python2.7'],
                    library_dirs = ['/usr/local/lib','/usr/lib'],
                    sources = allFiles)

with open('README') as file:
    readme = file.read()



setup (name = 'pollinotify',
       version = '0.1.0',
       description = 'inotify wrapper providing polling with timeout for specified filesystem events',
       author = 'Julian Porter',
       author_email = 'julian@jpembedded.solutions',
       url = 'http://jpembedded.solutions',
       platforms = 'linux',
       classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Environment :: No Input/Output (Daemon)',
          'Environment :: X11 Applications',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Filesystems',
          'Topic :: System :: Monitoring'
          ],
       ext_modules = [module1],
       test_suite='tests',
       long_description = readme
)
