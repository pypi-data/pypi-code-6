__author__ = 'Matt Clark'

with open('README.md') as f:
    long_desc = f.read()

from setuptools import setup
setup(
    name = "RDFdict",
    version = "0.1.6",
    py_modules = ['rdfdict'],

    # metadata for upload to PyPI
    author = "Matt Clark",
    author_email = "matt@mattclark.net",
    description = "A class for creating a nested dictionaries representation of RDF quads or triples",
    long_description = long_desc,
    license = "MIT",
    keywords = ['rdf','json', 'dict'],
    classifiers = ['Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Text Processing',
                   'License :: OSI Approved :: MIT License',
                   'Intended Audience :: Developers',
                   'Development Status :: 5 - Production/Stable',
                   'Operating System :: OS Independent'],
    url = "http://github.com/mattclarkdotnet/rdfdict"

)
