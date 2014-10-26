'''
Created on Feb 26, 2014

@author: zfyuan
'''

import numpy
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions = [Extension("countvar.rdiscrete",
                        ["countvar/rdiscrete.pyx"], 
                        include_dirs=[numpy.get_include()])
              ]

DESCRIPTION = """Sample algorithms for four kinds of univariate distributions, 
                 Poisson, Generalized Poisson, Zero Inflated Generalized Possion
                 and Negative Binomial Distribution."""

setup(
      name = 'countvar',
      version = '0.2.2',
      description = DESCRIPTION,
      author = "Zhenfei Yuan",
      author_email = "zf.yuan.y@gmail.com",
      license = 'GPL',
      packages = ['countvar'],
      ext_modules = cythonize(extensions)
)
