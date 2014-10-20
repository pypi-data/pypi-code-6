#!/usr/bin/env python

name = 'icheck'
path = 'icheck.py'


## Automatically determine project version ##
from setuptools import setup, find_packages
try:
    from hgdistver import get_version
except ImportError:
    def get_version():
        import os
        
        d = {'__name__':name}

        # handle single file modules
        if os.path.isdir(path):
            module_path = os.path.join(path, '__init__.py')
        else:
            module_path = path
                                                
        with open(module_path) as f:
            try:
                exec(f.read(), None, d)
            except:
                pass

        return d.get("__version__", 0.1)

## Use py.test for "setup.py test" command ##
from setuptools.command.test import test as TestCommand
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        pytest.main(self.test_args)


## Try and extract a long description ##
readme = ""
for readme_name in ("README", "README.rst", "README.md",
                    "CHANGELOG", "CHANGELOG.rst", "CHANGELOG.md"):
    try:
        readme += open(readme_name).read() + "\n\n"
    except (OSError, IOError):
        continue


## Finally call setup ##
setup(
    name = name,
    version = get_version(),
#    script_name = path,
    modules = [name],
    author = "Da_Blitz",
    author_email = "code@blitz.works",
    maintainer=None,
    maintainer_email=None,
    description = "Syntax checker for python using inotify",
    long_description = readme,
    license = "MIT BSD",
    keywords = "butter syntax check test",
    download_url="http://blitz.works/icheck",
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: BSD License",
                 "Operating System :: POSIX :: Linux",
                 "Programming Language :: Python :: 3",
                 "Topic :: Software Development :: Testing"
                ],
    platforms=None,
    url = "http://blitz.works",
    test_loader = "pytest:tests",
    test_suite = "all",

    entry_points = {"console_scripts":["icheck = icheck:entry_point",],
                   },

    include_package_data = True,
        
    zip_safe = True,
    setup_requires = ['hgdistver'],
    install_requires = ['butter>=0.9', "blessed>=1.9.4"],
    tests_require = ['pytest'],
    cmdclass = {'test': PyTest},
)
