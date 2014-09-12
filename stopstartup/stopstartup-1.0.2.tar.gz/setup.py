from setuptools import setup
from os.path import join

def readme():
    return open("README.rst").read()

setup(
    name = "stopstartup",
    description = "Stop services from starting",
    long_description = readme(),
    keywords = "stop services debian install",
    url = "https://github.com/wemash/stopstartup",
    version = "1.0.2",

    author = "Kenneth Pullen",
    author_email = "ken@mash.is",

    py_modules = ["stopstartup"],
    install_requires = ["Click"],
    entry_points = {"console_scripts": ["stopstartup = stopstartup:cli"]},
    data_files = [(join("/", "usr", "local", "stopstartup"), ["policy-rc.d"])],
)
