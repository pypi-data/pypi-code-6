import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires=['rauth']

setup(name='context-io-2',
    version='2.0.1',
    description='I did not create this package; I\'m just adding it to pypi.  It\'s already freely available on GitHub.',
    long_description=README,
    author='Tony Blank, Jesse Dhillon',
    author_email='tony@context.io, jesse@deva0.net',
    url='http://context.io',
    keywords=['contextIO', 'dokdok', 'imap', 'oauth'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)
