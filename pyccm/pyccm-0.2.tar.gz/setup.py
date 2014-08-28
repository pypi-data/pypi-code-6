# This Python file uses the following encoding: utf-8


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

from setuptools import setup, find_packages

package_name='pyccm'
setup(
       name = package_name,
       version = "0.2",
       packages=[package_name],
       package_dir = {package_name: 'lib'},
#
#        # metadata for upload to PyPI
        author = "F. B. Laliberté",
        author_email = "frederic.laliberte@utoronto.ca",
        description = "Implementation of the Convergent Cross Mapping (Sugihara et al., 2012: Detecting Causality in Complex Ecosystems, Science 338: 496–500.)",
        license = "BSD",
        keywords = "time series",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Science/Research",
            "Natural Language :: English",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 2.7",
            "Topic :: Scientific/Engineering :: Mathematics"
        ],
        long_description=read('README'),
        install_requires = ['numpy'],
        zip_safe=False,
    )
