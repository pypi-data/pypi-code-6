from setuptools import setup
import re
import stackq


def getREADME():
  with open("README.md") as README_FILE:
    return README_FILE.read()
  return stackq.__doc__


def lookupDependencies():
  with open("dependencies.txt") as depsFile:
    deps = depsFile.read()
    deps = re.sub("[<=>]+.*", "", deps)
    deps = deps.split("\n")
    return deps
  return []


setup(
  name="stackq",
  version=stackq.__version__,
  author="Forfuture LLC",
  author_email="we@forfuture.co.ke",
  url="https://github.com/stackq",
  download_url="https://github.com/forfuture-dev/stackq/zipball/master",
  description=stackq.__description__,
  keywords=["cli", "terminal", "stackoverflow", "stackexchange", "answers"],
  license="MIT",
  long_description=getREADME(),
  classifiers=[
    "Development Status :: 2 - Pre-Alpha",
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
#    "Programming Language :: Python :: 3"
#    "Programming Language :: Python :: 3.2"
#    "Programming Language :: Python :: 3.3"
#    "Programming Language :: Python :: 3.4"
  ],
  packages=["stackq"],
  install_requires=lookupDependencies(),
  entry_points={
    "console_scripts": ["stackq = stackq.stackq:run"]
  }
)
