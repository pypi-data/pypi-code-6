import os

from setuptools import setup, find_packages
from pip.req import parse_requirements

import bosun_foscam_plugins


# parse_requirements() returns generator of pip.req.InstallRequirement objects
path = os.path.abspath('requirements.txt')
install_reqs = parse_requirements(path)

# reqs is a list of requirement
reqs = [str(ir.req) for ir in install_reqs]

# load README.md
with open('README.md', 'r') as f:
    readme = f.read()


setup(
    name='bosun-foscam-plugins',
    version=bosun_foscam_plugins.__version__,
    author=bosun_foscam_plugins.__author__,
    description='Bosun plugins for the Foscam camera series to work with crowsnest.io',
    long_description=readme,
    url='https://github.com/crowsnest-io/bosun-foscam-plugins',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=reqs,
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Multimedia',
    ],
)
