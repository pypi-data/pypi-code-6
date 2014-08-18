#encoding:utf-8
import os
from setuptools import setup, find_packages


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

setup(
    name="sieve-sift",
    version="0.1.4",
    packages=find_packages(),
    scripts=["sift/sift", ],
    url="https://bitbucket.org/sievetech",
    license="",
    author="Sieve",
    author_email="sievetech@sieve.com.br",
    description="Sieve sift module.",
    data_files=[os.path.join(PROJECT_PATH, "sift", "sift"), ],
    install_requires=["matplotlib==1.2.0"]
)
