import os
import sys
from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


version = {}
with open("tutils/version.py") as fp:
    exec(fp.read(), version)
VERSION = version['__version__']

LICENSE = open("LICENSE").read().strip()


setup(
    name='tutils',
    version=VERSION,
    license=LICENSE,
    description='Utils',
    url='https://bitbucket.org/alexandrul/',
    author='Eduard-Cristian Stefan',
    author_email='alexandrul.ct@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    scripts=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        ],
    zip_safe=False,
    )
