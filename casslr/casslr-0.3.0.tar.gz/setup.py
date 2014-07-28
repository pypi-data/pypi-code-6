#coding:utf-8
import setuptools

name = "casslr"

with open("{0}/version.py".format(name)) as f:
    code = compile(f.read(), "version.py", "exec")
    exec(code)


setuptools.setup(
    name=name,
    version=__version__,
    packages=setuptools.find_packages(),
    url="https://github.com/scalr-tutorials/casslr",
    license="Apache 2.0",
    author="Thomas Orozco",
    author_email="thomas@scalr.com",
    long_description=open("README.rst").read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: Apache Software License",
    ],
    entry_points={},
    install_requires=["flask"],
    extras_require={},
    setup_requires=["nose"],
    tests_require=["tox", "nose"],
)
