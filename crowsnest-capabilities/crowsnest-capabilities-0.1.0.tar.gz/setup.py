import os

from setuptools import setup, find_packages
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
path = os.path.abspath('requirements.txt')
install_reqs = parse_requirements(path)

# reqs is a list of requirement
reqs = [str(ir.req) for ir in install_reqs]

# load README.md
with open('README.md', 'r') as f:
    readme = f.read()


setup(
    name='crowsnest-capabilities',
    version='0.1.0',
    author='Ian A Wilson',
    description='High-level language for Crowsnest API and plugin systm',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=reqs,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
)
