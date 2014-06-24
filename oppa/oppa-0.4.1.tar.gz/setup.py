#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(name         = "oppa",
      description  = "Presentation and lecture support tool",
      url          = "https://github.com/lkrotowski/oppa",
      version      = "0.4.1",
      packages     = find_packages("src"),
      package_dir  = {"": "src"},
      entry_points = {"console_scripts": ["oppa=oppa.main:main"]},
      author       = "Łukasz Krotowski",
      author_email = "lukasz.krotowski@gmail.com",
      license      = "GPLv3",
      classifiers  = ["Development Status :: 4 - Beta",
                      "Environment :: X11 Applications :: GTK",
                      "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                      "Operating System :: POSIX :: Linux",
                      "Topic :: Education :: Computer Aided Instruction (CAI)",
                      "Topic :: Multimedia :: Graphics :: Presentation"])
