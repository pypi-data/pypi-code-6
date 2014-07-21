#!/usr/bin/env python
# coding: utf-8

import os
from setuptools import setup, find_packages

entry_points = {"console_scripts": ["oppa=oppa.main:main"]}
if os.name == "nt":
	entry_points = {"console_scripts": ["oppa=oppa.main:main"],
	                "gui_scripts"    : ["oppaw=oppa.main:main"]}

setup(name         = "oppa",
      description  = "Presentation and lecture support tool",
      url          = "https://github.com/lkrotowski/oppa",
      version      = "0.5.0",
      packages     = find_packages("src"),
      package_dir  = {"": "src"},
      entry_points = entry_points,
      author       = "Łukasz Krotowski",
      author_email = "lukasz.krotowski@gmail.com",
      license      = "GPLv3",
      classifiers  = ["Development Status :: 4 - Beta",
                      "Environment :: Win32 (MS Windows)",
                      "Environment :: X11 Applications :: GTK",
                      "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                      "Operating System :: Microsoft :: Windows",
                      "Operating System :: POSIX :: Linux",
                      "Topic :: Education :: Computer Aided Instruction (CAI)",
                      "Topic :: Multimedia :: Graphics :: Presentation"])
