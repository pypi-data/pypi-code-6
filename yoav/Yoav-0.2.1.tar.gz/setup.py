import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



setup(
    name='Yoav',
    description='Yoavs Test Library',
    version='0.2.1', # NB: must be kept in sync with sift/version.py
    url='',

    author='Yoav Schatzberg',
    author_email='',
    long_description='',

    packages=['yoav'],
    install_requires=[
        "requests >= 0.14.1",
        "mock >= 1.0.1",
    ],

    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
