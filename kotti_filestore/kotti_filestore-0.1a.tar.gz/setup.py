import os

from setuptools import find_packages
from setuptools import setup

project = 'kotti_filestore'
version = '0.1a'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
CONTRIBUTORS = open(os.path.join(here, 'CONTRIBUTORS.rst')).read()

setup(
    name=project,
    version=version,
    description="Filesystem storage of BLOBs for Kotti.",
    long_description=README + '\n\n' + CONTRIBUTORS + '\n\n' + CHANGES,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Pylons",
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: User Interfaces",
        ],
    keywords='kotti',
    author='Andreas Kaiser',
    author_email='disko@binary-punks.com',
    url='https://github.com/disko/kotti_filestore',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Kotti>0.10b1',
        'repoze.filesafe',
        'yurl',
    ],
    entry_points={
        'scripts': [],
        },
    message_extractors={
        'foo': [
            ('**.py', 'lingua_python', None),
            ('**.zcml', 'lingua_xml', None),
            ('**.pt', 'lingua_xml', None),
        ]
    },
)
