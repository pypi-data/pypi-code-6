from setuptools import setup, Extension, Command
from setuptools.command.sdist import sdist
from setuptools.command.install import install

# my commands
def generate_modules():
    from Cython.Build import cythonize
    cythonize("pyfde/*.pyx")

class my_sdist(sdist):
    
    def run(self):
        generate_modules()
        sdist.run(self)

class my_install(install):
    
    def run(self):
        import os.path
        if not os.path.isfile('pyfde/solver.c'):
            generate_modules()
        
        install.run(self)

class my_clean(Command):
    
    description = "Removes the generated files from the directory"
    user_options = []
    
    def initialize_options(self):
        pass
    
    def run(self):
        import sys, os, glob, shutil

        patterns = ["pyfde/*.c", "pyfde/*.so", "pyfde/*.html", "MANIFEST"]
        for pat in patterns:
            for junk in glob.iglob(pat):
                try:
                    os.remove(junk)
                except:
                    pass

        dirs = ["pyfde/__pycache__", "tests/__pycache__", "PyFDE.egg-info",
                "build", "dist"]

        for dir in dirs:
            try:
                shutil.rmtree(dir, True)
            except:
                pass
    
    def finalize_options(self):
        pass

# information for the setup
with open('README.rst') as readme:
    long_description = readme.read()

import numpy

setup(
    name='PyFDE',
    version='0.4.0',
    description='A fast differential evolution module',
    author='Lucas Hermann Negri',
    author_email='lucashnegri@gmail.com',
    url='https://bitbucket.org/lucashnegri/pyfde',
    packages=['pyfde'],
    install_requires=['numpy'],
    ext_modules = [
        Extension("pyfde.solver", ["pyfde/solver.c"]),
        Extension("pyfde.bench", ["pyfde/bench.c"])
    ],
    cmdclass={
        'install' : my_install,
        'clean': my_clean,
        'sdist': my_sdist,
    },
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
