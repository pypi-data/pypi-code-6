from setuptools import *

setup(
    # Metadata
    name="babel-cli",
    version="0.3.0",
    author="Calder Coalson",
    author_email="caldercoalson@gmail.com",
    url="https://github.com/Calder/babel-cli",
    description = "Foo bar",
    long_description=open("README.txt").read(),
    license="LICENSE.txt",

    # Contents
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "babel=babel:main",
        ],
    },

    # Dependencies
    install_requires=[
        "requests-futures",
        "tmol",
        "twilio",
    ],

    # Settings
    zip_safe=True,
)

# # Hack to install script in /usr/local/bin on Mac OS X
# import sys
# if sys.prefix != "/usr/local/bin":
#     import subprocess
#     subprocess.call(["ln", "-sf",
#                      "%s/bin/babel" % sys.prefix,
#                      "/usr/local/bin/babel"])