import os
from setuptools import setup, Extension 

XAPIAN_INCLUDE = '/usr/local/xapian/include'
XAPIAN_SRC_BINDING = '/data0/sources/xapian-bindings'
XAPIAN_CORE_BINDING = '/data0/sources/xapian-core'
cmd = '/usr/local/bin/swig -python -c++ -I./include -I/usr/local/include -I' + XAPIAN_INCLUDE + ' -I' + XAPIAN_CORE_BINDING + ' -I' + XAPIAN_SRC_BINDING + ' -I' + XAPIAN_SRC_BINDING + '/python2.6 swig/distanceKeyMaker.i'
os.system(cmd)

module1 = Extension('_distanceKeyMaker',
        sources = ['swig/distanceKeyMaker_wrap.cxx','src/distanceKeyMaker.cpp'],
        include_dirs=['/data0/sources/xapian-core','/usr/local/include/python2.6','/usr/local/xapian/include','./include','/usr/local/include/'],
        libraries = ['xapian'],
        library_dirs = ['/usr/local/lib','/usr/local/xapian/lib']
        )

setup(
    name="distanceKeyMaker",
    version = "1.0.1",
    author = "lihaifeng",
    ext_modules = [module1]
)
