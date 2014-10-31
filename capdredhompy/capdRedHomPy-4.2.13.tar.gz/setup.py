from setuptools import setup, Extension
#from distutils.core import setup
#from distutils.extension import Extension
import os

# ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install  -e .


library_dirs = []

if 'CAPD_SRCDIR' in os.environ:
    import shutil

    for p in ['capdRedHom', 'src', 'tests']:
        if os.path.exists(p):
            shutil.rmtree(p)

    for p in ['capdRedHom', 'src', 'tests']:
        shutil.copytree(os.environ['CAPD_SRCDIR'] + '/python/' + p, p, shutil.ignore_patterns('*.pyc', '*~', '#*'))

    shutil.copy('version.py', 'capdRedHom/version.py')
else:
    pass



setup(name='capdRedHomPy',
      version='4.2.13',
      packages=[
          'capdRedHom',
          'capdRedHom.persistence',
      ],
      package_dir = {
          'capdRedHom' : 'capdRedHom',
          'capdRedHom.persistence' : 'capdRedHom/persistence',
      },
      ext_modules=[
          Extension('capdRedHom.api', ['src/api.cpp'],
                    language='C++',
                    library_dirs=library_dirs,
                    libraries=['capdapiRedHom_py'],
                )
      ],
      setup_requires=['nose>=1.0'],
      test_suite = 'nose.collector',
      )
