#!/usr/bin/python3
# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
try:
    from setuptools import setup
    using_setuptools = True
except ImportError:
    from distutils.core import setup
    using_setuptools = False

with open("README.rst", "r") as f:
    LONG_DESCRIPTION = f.read()

ABOUT = dict(
    name="android-debian-builder",
    version="1.0",
    description="Bootstrap a Debian system in a file, mostly for deploying to "
                "Android.",
    author="Felix Krull",
    author_email="f_krull@gmx.de",
    url="https://bitbucket.org/fk/android-debian-builder",
    platforms=["Debian"],
    long_description=LONG_DESCRIPTION,
    license="MIT",
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Android",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Installation/Setup",
    ],
)

PACKAGES = ["android_debian_builder"]
PACKAGE_DATA = {"android_debian_builder": ["data/*", "examples/*"]}
INSTALL_REQUIRES = ["Jinja2 >= 2.7"]
ENTRY_POINTS = {
    "console_scripts": [
        "android-debian-builder=android_debian_builder.script:main",
    ],
}
SCRIPTS = ["android-debian-builder"]

if __name__ == "__main__":
    args = {}
    args.update(ABOUT)
    args.update(
        packages=PACKAGES,
        package_data=PACKAGE_DATA,
        scripts=SCRIPTS
    )
    if using_setuptools:
        args.update(
            install_requires=INSTALL_REQUIRES,
            entry_points=ENTRY_POINTS,
            zip_safe=False
        )

    setup(**args)
