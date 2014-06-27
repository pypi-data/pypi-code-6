from distutils.core import setup
from setuptools import find_packages

setup(
    name="beret",
    version="0.2.1",
    author="Eric Chiang",
    author_email="info@yhathq.com",
    url="https://github.com/yhat/beret",
    packages=find_packages(),
    description="Parse a csv file and score through a yhat model",
    license="BSD",
    scripts=["bin/beret"],
    install_requires=[
        "docopt>=0.6.1",
        "pandas==0.13.0",
        "requests>=2.3.0",
        "yhat>=1.0.0"
    ]
)
