#!/usr/bin/env python
from distutils.core import setup


setup(
    name = "py-execute",
    packages = ["py_execute"],
    version = "0.1.3",
    description = "External process executor wrapper",
    author = "Julia S.Simon",
    author_email = "julia.simon@biicode.com",
    url = "https://github.com/biicode/py-execute",
    download_url = "https://pypi.python.org/packages/source/p/py-execute/py-execute-0.1.tar.gz",
    keywords = ["process", "execute", "output"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "Topic :: Terminals",
        "Topic :: Utilities",
        ],
    long_description = """\
External Process Execution Wrapper
-----------------------------------

Allows you to execute external commands getting large outputs in real-time but also getting
all the output as a return variable.


Examples
--------

    from py_execute import run_command
    ret = run_command.execute('echo "Hello World"')
        Hello World
    ret
        'Hello World\n'

    ret = run_command.execute('read -p "Do you like py-executor?" yn; case $yn in [yY]* ) echo "cool";; esac', user_input='y\n')
        cool
    ret
        'cool\n'
"""
)
