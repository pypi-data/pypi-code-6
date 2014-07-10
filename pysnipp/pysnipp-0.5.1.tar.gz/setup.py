import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('pysnipp/pysnipp.py').read(),
    re.M
    ).group(1)

setup(
    name='pysnipp',
    version=version,
    packages=['pysnipp'],
    entry_points = {
                 "console_scripts": ['pysnipp = pysnipp.pysnipp:main']
                    },
    install_requires = [
                'redis',
                'docopt'
                        ],
    url="http://hauck-daniel.de/pysnipp",
    license='GPL',
    author='Daniel Hauck',
    author_email='daniel@hauck.it',
    description='console based snippet manager written in python3'
)
