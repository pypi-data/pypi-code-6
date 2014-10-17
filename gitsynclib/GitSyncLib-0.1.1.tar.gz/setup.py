# -*- encoding: utf8 -*-
import glob
import io
import re
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()

setup(
    name='GitSyncLib',
    version="0.1.1",
    license='MIT',
    description='GitSyncLib is a library that supports GitSync.',
    long_description="%s\n%s" % (read("README.rst"), re.sub(":obj:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst"))),
    author='Jachin Rupe',
    author_email='jachin@clockwork.net',
    url="https://github.com/jachin/GitSyncLib",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(i))[0] for i in glob.glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Communications :: File Sharing',
        'Topic :: Utilities',
    ],
    install_requires=[
        "Fabric >= 1.3.2",
        "PyYAML >= 3.10",
    ],
)
