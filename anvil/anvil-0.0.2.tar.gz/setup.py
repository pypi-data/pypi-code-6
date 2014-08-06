from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

version_file = open(os.path.join(here, 'anvil', 'VERSION'))
version = version_file.read().strip()

# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='anvil',

    # Versions should comply with PEP440. For single-sourced versioning, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version=version,

    description='Generates new project structures from Jinja templates',
    long_description=long_description,

    # The project URL.
    url='https://github.com/dghubble/anvil',

    # Author details
    author='Dalton Hubble',
    author_email='dghubble@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
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
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords=('anvil', 'generate', 'project', 'template', 'skeleton',
              'package', 'app', 'plugin', 'jinja', 'jinja2'),

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['anvil'],

    # Run-time package dependencies. These will be installed by pip when your
    # project is installed.
    install_requires=[
        'jinja2>=2.7.3',
        'pyyaml>=3.11'
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'anvil=anvil.cli:main',
        ],
    },

    # MANIFEST.in included entries should be included as package data and
    # installed into site-packages 
    include_package_data=True,

    # Default to False unless you specifically intend the package to be
    # installed as an .egg
    zip_safe=False,
)
