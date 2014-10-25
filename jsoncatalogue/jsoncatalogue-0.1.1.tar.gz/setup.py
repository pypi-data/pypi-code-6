from setuptools import setup

description = ("Local filesystem based JSON catalogue,"
               " usable e.g. with package `jsonschema`")
with open("README.rst") as f:
    long_description = f.read()

version = "0.1.1"
setup(
    name='jsoncatalogue',
    description=description,
    version=version,
    url="https://bitbucket.org/vlcinsky/sh-jsoncatalogue",
    author='Jan Vlcinsky',
    author_email='jan.vlcinsky@cdv.cz',
    long_description=long_description,
    py_modules=["jsoncatalogue"],
    include_package_data=True,
    zip_safe=False,
    license="MIT"
)
