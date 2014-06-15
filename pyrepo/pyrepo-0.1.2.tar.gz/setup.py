from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

version_file = open(os.path.join(here, 'pyrepo', 'VERSION'))
version = version_file.read().strip()

# Get the long description from the relevant file
with codecs.open('DESCRIPTION.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyrepo',

    # Versions should comply with PEP440. For single-sourced versioning, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version=version,

    description='Python repository abstraction',
    long_description=long_description,

    # The project URL.
    url='https://github.com/dghubble/pyrepo',

    # Author details
    author='Dalton Hubble',
    author_email='dghubble@gmail.com',

    # Choose your license
    license='MIT',

    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        # Project maturity. 
        'Development Status :: 3 - Alpha',

        # Intended audience
        'Intended Audience :: Developers',

        # Topic
        'Topic :: Software Development :: Build Tools',

        # License should match "license" above
        'License :: OSI Approved :: MIT License',

        # Python versions supported
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='repo repository vcs git mercurial hg svn subversion bazaar',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages.
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # Run-time package dependencies.
    install_requires = [],
)
