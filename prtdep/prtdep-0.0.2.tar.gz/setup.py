import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


import prtdep.prtdep as pd


setup(
    name='prtdep',
    version=pd.__version__,
    author='Darko Poljak',
    author_email='darko.poljak@gmail.com',
    description='CRUX ports dependencies helper.',
    license="GPLv3",
    keywords=['ports dependencies helper', ],
    url='https://github.com/darko-poljak/prtdep',
    download_url='https://github.com/darko-poljak/prtdep',
    packages=['prtdep'],
    entry_points={
        'console_scripts': [
            'prtdep=prtdep.prtdep:main',
        ],
    },
    long_description=read('README.rst'),
    platforms="OS Independent",
    install_requires=["docopt"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: System :: Systems Administration",
    ],
)
