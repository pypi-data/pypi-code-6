import os
import re

from setuptools import setup, find_packages

# Do not try to import the package to get its version.
_version_file = open(os.path.join(os.path.dirname(__file__), 'dokang_pdf', 'version.py'))
VERSION = re.compile(r"^VERSION = '(.*?)'", re.S).match(_version_file.read()).group(1)


def load_requirements(path):
    reqs = []
    with open(path) as fp:
        reqs = [line for line in fp.read().split("\n")
            if line and not line.startswith(("-r", "#"))]
    return reqs


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read().strip()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read().strip()

setup(name='dokang_pdf',
      version=VERSION,
      description="PDF harvester for Dokang",
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        # PDFMiner does not support Python 3.
        ],
      author="Polyconseil",
      author_email="opensource+dokang@polyconseil.fr",
      url='',
      keywords='full-text search engine',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=load_requirements('requirements.txt'),
      tests_require=load_requirements('requirements_dev.txt'),
      test_suite='tests',
      )
