#!/usr/bin/env python
from setuptools import setup

import bandstructureplot

setup(name="bandstructureplot",
      version=bandstructureplot.__version__,
      description="A Lightweight Band Structure Plotting Library",
      author="Shudan Zhong",
      author_email="shudan@shudan.me",
      py_modules=['bandstructureplot'],
      license='GPLv3 or later',
      install_requires=[
          "numpy >= 1.7.1",
          "matplotlib >= 1.2.1",
],)
