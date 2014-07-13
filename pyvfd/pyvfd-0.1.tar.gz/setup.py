from distutils.core import setup
setup(
    name = "pyvfd",
    version = "0.1",
    author = "David Farler",
    author_email = "accumulator@icloud.com",
    maintainer = "David Farler",
    maintainer_email = "accumulator@icloud.com",
    url = 'https://github.com/magaio/pyvfd',
    description = "Serial module for the NEC FC20X2JA-AB",
    packages = ["vfd"],
    download_url = "https://github.com/magaio/pyvfd/releases/download/v0.1/pyvfd-0.1.tar.gz",
    license = 'BSD',
    long_description = """\
Python module for the NEC FC20X2JA-AB
-------------------------------------
See the enclosed README.md and datasheet for more information.

This version requires Python 3 or later.
"""
)
