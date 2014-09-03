# coding=utf8

from setuptools import setup

setup(
    name='thriftr',
    version='0.0.1',
    author='hit9',
    author_email='nz2324@126.com',
    description='Pure python apache thrift parser',
    packages=['thriftr'],
    url='https://github.com/hit9/thriftr.git',
    license='MIT',
    install_requires=['ply'],
    zip_safe=False,
    classifiers=[
        "Topic :: Software Development",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
