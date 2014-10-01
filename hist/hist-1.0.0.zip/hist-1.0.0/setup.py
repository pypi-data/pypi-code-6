# to distribute:
# python setup.py register sdist upload

from setuptools import setup
import sys
import os

try:
    ## Remove 'MANIFEST' file to force
    ## distutils to recreate it.
    ## Only in "sdist" stage. Otherwise
    ## it makes life difficult to packagers.
    if sys.argv[1] == "sdist":
        os.unlink("MANIFEST")
except:
    pass

setup(
    name="hist",
    version="1.0.0",
    scripts=['hist'],
    author="Ron Reiter",
    author_email="ron@crosswise.com",
    url="http://github.com/crosswise/hist",
    license="MIT",
    description="hist generates histograms from a list of numbers",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
    install_requires=["matplotlib==1.1.1"],
)
