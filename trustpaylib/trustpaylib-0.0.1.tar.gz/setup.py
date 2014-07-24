# -*- coding: utf-8 -*-
# vim:fenc=utf-8


from setuptools import setup


with open("README.rst") as f:
    description = f.read()

setup(
    version="0.0.1",
    name="trustpaylib",
    description="TrustPay payments integration library.",
    long_description=description,
    author="Michal Kuffa",
    author_email="michal.kuffa@gmail.com",
    py_modules=["trustpaylib"],
    license="BSD",
    url="https://github.com/beezz/trustpaylib",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
    ]
)
