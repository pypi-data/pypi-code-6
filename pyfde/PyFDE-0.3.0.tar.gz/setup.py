try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from Cython.Build import cythonize

with open('README.rst') as readme:
    long_description = readme.read()

import numpy

setup(
    name='PyFDE',
    version='0.3.0',
    description='A fast differential evolution module',
    author='Lucas Hermann Negri',
    author_email='lucashnegri@gmail.com',
    url='https://bitbucket.org/lucashnegri/pyfde',
    packages=['pyfde'],
    install_requires=['numpy', 'cython'],
    ext_modules = cythonize("pyfde/*.pyx"),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    license="MIT",
    include_dirs=[numpy.get_include()]
 )

# ahh, so clean
import sys
import os
import glob
import shutil

if "clean" in sys.argv:
    print("removing junk")

    patterns = ["pyfde/*.c", "pyfde/*.so", "pyfde/*.html", "MANIFEST"]
    for pat in patterns:
        for junk in glob.iglob(pat):
            os.remove(junk)

    dirs = ["pyfde/__pycache__", "tests/__pycache__", "PyFDE.egg-info",
            "build", "dist"]

    for dir in dirs:
        shutil.rmtree(dir, True)
