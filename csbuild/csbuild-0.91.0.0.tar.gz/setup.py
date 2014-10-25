from distutils.core import setup
from distutils.sysconfig import get_python_lib
import datetime

with open("csbuild/version", "r") as f:
      csbuild_version = f.read().strip()

setup(name='csbuild',
      version=csbuild_version,
      #py_modules=['csbuild'],
      packages=["csbuild"],
      package_data={"csbuild":["version", "*.py"]},
      author="Jaedyn K. Draper",
      author_email="jaedyn.pypi@jaedyn.co",
      url="https://github.com/3jade/csbuild",
      description="C/C++ build tool",
      long_description="CSBuild is a C/C++ build system that attempts to improve over existing build solutions by providing improvements to build speed, makefile syntax, cross-platform support, analytics, and extensibility.",
      classifiers=[
         "Development Status :: 4 - Beta",
         "Environment :: Console",
         "Intended Audience :: Developers",
         "License :: OSI Approved :: MIT License",
         "Natural Language :: English",
         "Operating System :: POSIX :: Linux",
         "Programming Language :: C",
         "Programming Language :: C++",
         "Programming Language :: Python :: 2.7",
         "Programming Language :: Python :: 3.2",
         "Programming Language :: Python :: 3.3",
         "Programming Language :: Python :: 3.4",
         "Topic :: Software Development :: Build Tools"
      ]
      )
