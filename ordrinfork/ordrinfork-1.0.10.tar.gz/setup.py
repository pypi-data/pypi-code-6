import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup

import sys
if not (sys.version_info.major == 2 and sys.version_info.minor == 7):
    print "This package only works with Python 2.7"
    exit()

setup(
    name="ordrinfork",
    version='1.0.10',
    packages=['ordrinfork'],
    include_package_data=True,
    py_modules=['distribute_setup'],
    description="Ordr.in API Client",
    author="Ordr.in",
    author_email="don.hcd@gmail.com",
    # url="https://github.com/ordrin/api-py",
    install_requires=['urllib3', 'jsonschema'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 4 - Beta",
        "Topic :: Software Development",
        "Topic :: Internet"
    ]
)
