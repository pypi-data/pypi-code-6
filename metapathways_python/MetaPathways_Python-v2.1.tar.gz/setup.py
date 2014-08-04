import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "MetaPathways_Python",
    version = "v2.1",
    author = "Niels Hanson, Kishori Konwar",
    author_email = "kishori82@gmail.com",
    description = ("A pipeline for MetaGenomic analysis which is capable of creating ePGDBs using Pathway Tools"),
    license = "BSD",
    keywords = "metagenomics metapathways pathwaytools epgdb pgdb",
    url = "http://packages.python.org/metapathwaysv2",
    #packages= ['metapathways2'],
    packages = find_packages(),
    long_description=read('README'),
    classifiers=[],
)
