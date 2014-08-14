from setuptools import setup, find_packages
from os import path
import re

# Get current path
here = path.abspath(path.dirname(__file__))

# Get version from strikepackage.py
with open(path.join(here, 'strikepackage/strikepackage.py')) as f:
    version_file = f.read()
version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                          version_file, re.M)
if version_match:
    version = version_match.group(1)
else:
    raise RuntimeError("Unable to find version string.")

# Get long description from README and HISTORY
with open(path.join(here, 'README.rst')) as f:
    readme = f.read()
with open(path.join(here, 'HISTORY.rst')) as f:
    history = f.read()

# Dependencies
requires = [
    'Jinja2',
    'docopt',
    'kaptan',
    'requests',
    'progress',
    'python-simple-hipchat',
    'schema',
    'XenAPI',
    'PyYAML',
]

# Setup
setup(
    name='strikepackage',
    version=version,
    description='A command line tool to deploy virtual machines on XenServer.',
    long_description=readme + '\n\n' + history,
    author='Paul Liu',
    author_email='paul@ferociouspings.com',
    url='https://github.com/pwyliu/strikepackage',
    license='MIT',
    zip_safe=False,  # fuck an egg
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Operating System :: POSIX :: Linux',
    ],
    keywords='XenServer XenAPI virtualization automation',
    install_requires=requires,
    include_package_data=True,
    packages=find_packages(),
    package_data={'examples': ['*.yaml', '*.jinja2']},
    entry_points={
        'console_scripts': ['strikepackage = strikepackage.strikepackage:main']
    },
)
