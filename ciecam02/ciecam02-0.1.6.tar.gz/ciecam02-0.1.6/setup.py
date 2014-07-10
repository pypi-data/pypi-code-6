from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy as np
ext_modules = [
    Extension("ciecam02",
              ["ciecam02/ciecam02.pyx",],
              libraries=["m"],
              include_dirs=[np.get_include()]
          )
]
setup(
    #ext_modules = cythonize("glcprocedure.pyx")
    name = "ciecam02",
    version = '0.1.6',
    py_modules = ["ciecam02"],
    author = 'Dannyv',
    author_email = 'yu.yuyudan@gmail.com',
    packages = ["ciecam02",],
    license = 'BSD licence',
    description = 'a set of function convert colorspace among rgb, ciexyz, ciecam02 for python2.7',
    long_description = open('README.txt').read(),
    cmdclass = {"build_ext": build_ext},
    ext_modules = ext_modules
)
