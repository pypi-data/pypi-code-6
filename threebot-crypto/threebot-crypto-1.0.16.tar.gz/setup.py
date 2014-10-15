# -*- encoding: utf-8 -*-
from setuptools import setup

setup(
    name="threebot-crypto",
    packages=['threebot_crypto'],
    version="1.0.16",
    author_email="wagner@arteria.ch",
    maintainer_email="admin@arteria.ch",
    install_requires=[
        "pycrypto>=2.6.1",
        "msgpack-python>=0.4.1"
    ],
)
