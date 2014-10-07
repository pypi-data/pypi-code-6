# pytui's setup.py
from distutils.core import setup
setup(
    name = "pytui",
    packages = ["pytui"],
    version = "0.0",
    description = "python terminal user interface",
    author = "mohammad alghafli",
    author_email = "thebsom@gmail.com",
    url = "http://pypi.python.org/pypi/pytui",
    install_requires = ["colorama"],
    keywords = ["terminal", "user", "interface"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Terminals",
        "Topic :: Software Development :: User Interfaces",
        ],
    long_description = """
Python Terminal User Interface
-------------------------------------

Pytui is a user interface library that works in the terminal. It understands label boxes, Text boxes and List boxes and draws them by coloring the terminal. It also monitors keyboard inputs and calls handlers to them.

Pytui requires Python 3.4. It also depends on colorama library to support windows system.

This library was made to be part of a programming tutorial. I tried to make it a little general purpose but focused on a chat program I made for the tutorial. It may need more tweaks.

A tutorial should be written at some point.
"""
)
