#!/usr/bin/env python
import os
import setuptools


here = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(here, "scalr_client_core", "version.py")) as f:
    code = compile(f.read(), "version.py", "exec")
    exec(code)


setuptools.setup(
    name="scalr-client-core",
    version=__version__,
    packages=setuptools.find_packages(),
    license="Proprietary",
    author="Thomas Orozco",
    author_email="thomas@scalr.com",
    description="Low-level client library for the Scalr API",
    install_requires=["geventhttpclient==1.1.0", "xmltodict==0.9.0"],
    setup_requires=["nose"],
    tests_require=["nose", "tox"],
    url="http://www.scalr.com"
)
