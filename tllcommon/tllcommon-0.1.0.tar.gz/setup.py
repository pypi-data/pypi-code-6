import setuptools
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt')
requirements = [str(ir.req) for ir in install_reqs]

setuptools.setup(
    name="tllcommon",
    version="0.1.0",
    url="https://github.com/timelinelabs/tll-common",

    author="Chris Goller",
    author_email="goller@timelinelabs.com",

    description="Low-level, reshareable Python code for Timeline Labs projects",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=requirements,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests'
)
