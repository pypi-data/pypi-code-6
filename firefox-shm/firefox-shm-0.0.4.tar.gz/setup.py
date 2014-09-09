import codecs
import os
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    # https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


long_description = read("README.rst")


# setup a list to scripts which are run as standalone 
scripts = ["scripts/firefox-shm"]

setup(
    name="firefox-shm",
    version=find_version("firefox_shm", "__version__.py"),
    long_description=long_description,
    description="Helper scripts for my linux system.",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.3",
        "Topic :: System :: Systems Administration",
    ],
    keywords=["firefox tmpfs"],
    author="Jens Kasten",
    author_email="jens@kasten-edv.de",
    url="http://bitbucket.org/igraltist/firefox-shm",
    license="GNU GPLv3",
    scripts=scripts,
    package_dir={"firefox_shm": "firefox_shm"},
    packages=["firefox_shm"],
    zip_safe=False
)
