#!/usr/bin/env python

from distutils.core import Extension, setup

sources = ['config.cpp', 'crypto.cpp', 'page.cpp', 'rand.cpp', 'text.cpp', 'otpnitro.i']

setup(name = 'otpnitro',
      version = '1.0',
      description = 'Python wrapper for the otpnitro crypto library',
      author = 'capi_x',
      author_email = 'capi_x@haibane.org',
      url = 'http://www.haibane.org/',
      py_modules = ['otpnitro'],
      ext_modules = [Extension(name='_otpnitro',
                               sources=sources,
                               swig_opts=['-c++', '-I.'],
                               include_dirs=['.'])],
     )