#!/usr/bin/env python

from setuptools import setup, find_packages


from hipachectl.version import version


setup(
    name="hipachectl",
    version=version,
    description="Command Line Tool to Manage hipache",
    long_description=open("README.rst", "r").read(),
    author="James Mills",
    author_email="James Mills, prologic at shortcircuit dot net dot au",
    url="https://bitbucket.org/prologic/hipachectl",
    download_url="http://bitbucket.org/prologic/hipachectl/downloads/",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    license="MIT",
    keywords="hipache manage docker",
    platforms="POSIX",
    packages=find_packages("."),
    install_requires=list(open("requirements.txt", "r")),
    entry_points={
        "console_scripts": [
            "hipachectl=hipachectl.main:main"
        ]
    },
    zip_safe=True
)
