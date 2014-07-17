# Simple setup script.

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Build.Dependencies import create_extension_list
import os
import numpy

source_files = ["pyppapi/ppapi_wrapper.pyx",
                "pyppapi/stub.cpp",
                "pyppapi/conn_stubs.c"]
extensions = [Extension("pyppapi/ppapi_wrapper", source_files,
                        language = "c++",
                        include_dirs = [numpy.get_include()])]
modules = cythonize(extensions)
for module in modules:
    print module
    module.language = "c++"
    print module.language

setup(name='pyppapi',
      version='0.5',
      description='Wrapper for some PPAPI functions.',
      url='http://bitbucket.org/zeropy/pyppapi',
      author='Matthew J. Turk',
      author_email='matthewturk@gmail.com',
      license='BSD',
      packages=['pyppapi'],
      ext_modules=cythonize(modules),
)

