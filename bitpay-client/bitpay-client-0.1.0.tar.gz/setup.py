from distutils.core import setup
#from setuptools import setup
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()
setup(
    name='bitpay-client',
    version='0.1.0',
    description='Python client for the BitPay payment web API distributed via PyPi',
    long_description="New usage: from bitpay-client import bp_lib\n" + read_md( 'README.md' ),
    maintainer='kiddhustle',
    maintainer_email='kiddhustle@wiardweb.com',
    url="https://github.com/bitpay/python-client",
    packages=['bitpay-client'],
)