import os
from distutils.core import setup

# sync with __init__.py
version = '1.0'

setup(
    name="dyn-python",
    version=version,
    keywords=["dyn", "dynect", "api", "dns", "traffic", "email", "messaging"],
    long_description=open(os.path.join(os.path.dirname(__file__),"README.md"), "r").read(),
    description="Dyn Python SDK",
    author="Carl Levine, Sunny Gleason, Cole Tuininga",
    author_email="clevine@dyn.com",
    url="https://github.com/dyninc/dyn-python",
    packages=['dyn'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: Software Development :: Libraries', 
    ],
)
