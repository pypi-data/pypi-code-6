from distutils.core import setup
from setuptools import find_packages


required = []

setup(
    name="zdb",
    version="0.1.0",
    author="Greg Lamp",
    author_email="greg@yhathq.com",
    url="https://github.com/yhat/zdb/",
    license=open("LICENSE.txt").read(),
    packages=find_packages(),
    package_dir={"zdb": "zdb"},
    package_data={"zdb": []},
    description="a db package that doesn't suck",
    long_description=open("README.rst").read(),
    install_requires=required,
)

