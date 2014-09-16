##############################################################################
#
# Copyright (c) 2008 Kapil Thangavelu
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import os, setuptools, shutil, urllib2, zipfile

rname = 'yui_2.9.0'
url_base = 'http://yui.github.io/yui2/archives'
version = '0.5.4'
prefix = 'yui/'
include_parts = ['/assets', '/build']

dest = os.path.join(os.path.dirname(__file__),
                    'src', 'ore', 'yui', 'resources')
                    
                    
extpaths = []
print dest
if not os.path.exists(dest):
    zip_name = rname + '.zip'
    print zip_name
    if not os.path.exists(zip_name):
        pkg_url = url_base+'/'+zip_name
        x = urllib2.urlopen( pkg_url ).read()
        open(zip_name, 'w').write(x)

    zfile = zipfile.ZipFile(zip_name, 'r')
    lprefix = len(prefix)-1

    for zname in sorted(zfile.namelist()):
        assert zname.startswith(prefix)
        zname_part = zname[lprefix:]
        include_p = False
        for pi in include_parts:
            if zname_part.startswith( pi ):
                include_p = True
        if not include_p: continue
        dname = dest + zname_part
        if dname[-1:] == '/':
            os.makedirs(dname)
        else:
            open(dname, 'w').write(zfile.read(zname))
            extpaths.append('yui/'+zname[lprefix:])
else:
    lbase = len(os.path.dirname(dest))+1
    for path, dirs, files in os.walk(dest):
        prefix = path[lbase:]
        for file in files:
            extpaths.append(os.path.join(prefix, file))

def read(*rnames):
    file_path = os.path.join(os.path.dirname(__file__), *rnames)
    return open( file_path ).read()

setuptools.setup(
    name = 'ore.yui',
    version = version,
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description = "Zope3 Package of the YUI library",
    long_description=( read('src','ore','yui','README.txt')
                       + '\n\n' +
                       read('changes.txt')
                       ),
    url='http://pypi.python.org/pypi/ore.yui',
    namespace_packages = ['ore'],
    packages = setuptools.find_packages('src'),
    package_dir = {'':'src'},
    include_package_data = True,
    zip_safe=False,
    package_data = {'ore.yui': extpaths},    
    install_requires = [
        'setuptools',
        'zope.viewlet',
        'zc.resourcelibrary',
        ],
    classifiers=['Programming Language :: Python',
                 'Environment :: Web Environment',
                 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                 'Framework :: Zope3',
                 ],    
    )
