from distutils.core import setup
from Cython.Build import cythonize

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name='PyFDE',
    version='0.2.0',
    description='A fast differential evolution module',
    author='Lucas Hermann Negri',
    author_email='lucashnegri@gmail.com',
    url='https://bitbucket.org/lucashnegri/pyfde',
    packages=['pyfde'],
    requires=['numpy', 'cython'],
    ext_modules = cythonize("pyfde/*.pyx"),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    license="MIT"
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

    dirs = ["pyfde/__pycache__", "tests/__pycache__"]

    for dir in dirs:
        shutil.rmtree(dir, True)
