import os
from setuptools import setup, find_packages

# package meta info
NAME = "arbitor"
VERSION = "0.1.5"
DESCRIPTION = ""
AUTHOR = "Haochuan Guo"
AUTHOR_EMAIL = "guohaochuan@gmail.com"
LICENSE = "BSD"
URL = "https://github.com/eleme/arbitor"
KEYWORDS = "etcd"
REQUIREMENTS = "python-etcd"

# package contents
PACKAGES = find_packages(
    exclude=['tests.*', 'tests', 'examples.*', 'examples',
             'dev_requirements.txt'])

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    install_requires=REQUIREMENTS,
    license=LICENSE,
    url=URL,
    keywords=KEYWORDS,
    packages=PACKAGES,
    install_package_data=True,
    zip_safe=False,
)
