import sys
from setuptools import setup
import ultralite

if sys.version_info < (3,3):
    raise NotImplementedError("ultralite is written for Python 3.3+.")

setup(
    name='ultralite',
    description="A tiny, inline-able http module mimicing requests' core API.",
    long_description=ultralite.__doc__,
    version="0.1.1",
    url="https://github.com/cathalgarvey/ultralite",
    author="Cathal Garvey",
    author_email="cathalgarvey@cathalgarvey.me",
    maintainer="Cathal Garvey",
    maintainer_email="cathalgarvey@cathalgarvey.me",
    license="GNU Affero General Public License v3",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Environment :: Console",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4"
    ]
)
