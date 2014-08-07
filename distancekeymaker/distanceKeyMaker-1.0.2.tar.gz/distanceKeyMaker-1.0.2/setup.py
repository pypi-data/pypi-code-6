import os
from setuptools import setup, Extension ,find_packages

#XAPIAN_INCLUDE = '/usr/local/xapian/include'
#XAPIAN_SRC_BINDING = './src/xapian-bindings'
#XAPIAN_CORE_BINDING = './src/xapian-core'
#cmd = '/usr/local/bin/swig -python -c++ -I./include -I/usr/local/include -I' + XAPIAN_INCLUDE + ' -I' + XAPIAN_CORE_BINDING + ' -I' + XAPIAN_SRC_BINDING + ' -I' + XAPIAN_SRC_BINDING + '/python2.6 swig/distanceKeyMaker.i'
#os.system(cmd)

module1 = Extension('_distanceKeyMaker',
        sources = ['swig/distanceKeyMaker_wrap.cxx','src/distanceKeyMaker.cpp'],
        include_dirs=['./src/xapian-core','/usr/local/include/python2.6','/usr/local/xapian/include','include','/usr/local/include/','swig','./src/xapian-bindings/python/','./src/xapian-core'],
        libraries = ['xapian'],
        library_dirs = ['/usr/local/lib','/usr/local/xapian/lib']
        )

module2 = Extension('_distanceKeyMaker',
        sources = ['src/distanceKeyMaker.cpp','swig/distanceKeyMaker.i'],
        swig_opts=['-c++', '-I./include','-I/usr/local/include','-I/usr/local/xapian/include','-I./src/xapian-bindings/python/','-I./src/xapian-bindings/','-I./src/xapian-core'],
        include_dirs=['./src/xapian-core','/usr/local/include/python2.6','/usr/local/xapian/include','include','/usr/local/include/','swig','./src/xapian-bindings/python/','./src/xapian-core'],
        libraries = ['xapian'],
        library_dirs = ['/usr/local/lib','/usr/local/xapian/lib']
        )
setup(
    name="distanceKeyMaker",
    #packages=find_packages(),
    packages = ['distanceKeyMaker'],
    package_dir={'distanceKeyMaker': 'src'},
    package_data={'distanceKeyMaker': ['xapian-core/*.h','xapian-bindings/*.i']},
    version = "1.0.2",
    author = "lihaifeng",
    ext_modules = [module2]
)
