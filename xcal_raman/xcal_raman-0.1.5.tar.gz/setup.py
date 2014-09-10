#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name="xcal_raman",
      version="0.1.5",
      description="Module for x-axis calibration of Raman spectrometers",
      author="Roman Kiselev",
      author_email="roman.kiselew@gmail.com",
      py_modules=["xcal_raman", "winspec"],
      scripts=[],
      license="GNU GPL v3",
      url="https://pypi.python.org/pypi/xcal_raman",
      platforms=["Linux", "Windows"],
      requires=[
              "numpy",
              "pylab",
              "scipy",
          ],
      classifiers=[
              "Development Status :: 2 - Pre-Alpha",
              "Topic :: Scientific/Engineering :: Physics",
              "Topic :: Scientific/Engineering :: Chemistry",
          ],
     )
