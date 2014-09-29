import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'requirements.txt')) as f:
    requires = filter(None, f.readlines())

setup(
    name='unicore-gitmodels',
    version='1.4.0',
    description='Definition of models used for python-gitmodel',
    long_description=
    open('README.rst', 'r').read() +
    open('AUTHORS.rst', 'r').read() +
    open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/unicore-gitmodels',
    packages=find_packages(),
    install_requires=requires,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
