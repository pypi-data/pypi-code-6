#!/usr/bin/env python
import os
import setuptools


here = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(here, "scalr_client_core", "version.py")) as f:
    code = compile(f.read(), "version.py", "exec")
    exec(code)

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join)
    in a platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

EXCLUDE_FROM_PACKAGES = []

def is_package(package_name):
    for pkg in EXCLUDE_FROM_PACKAGES:
        if package_name.startswith(pkg):
            return False
    return True

# Compile the list of packages and data available, because distutils doesn't have
# an easy way to do this (at least not for the data).
packages, package_data = [], {}

root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
package_dir = 'scalr_client_core'

for dirpath, dirnames, filenames in os.walk(package_dir):
    # Ignore PEP 3147 cache dirs and those whose names start with '.'
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
    parts = fullsplit(dirpath)
    package_name = '.'.join(parts)
    if '__init__.py' in filenames and is_package(package_name):
        packages.append(package_name)
    elif filenames:
        relative_path = []
        while '.'.join(parts) not in packages:
            relative_path.append(parts.pop())
        relative_path.reverse()
        path = os.path.join(*relative_path)
        package_files = package_data.setdefault('.'.join(parts), [])
        package_files.extend([os.path.join(path, f) for f in filenames])

setuptools.setup(
    name="scalr-client-core",
    version=__version__,
    packages=packages,
    package_data=package_data,
    license="Proprietary",
    author="Thomas Orozco",
    author_email="thomas@scalr.com",
    description="Low-level client library for the Scalr API",
    install_requires=["geventhttpclient==1.1.0", "xmltodict==0.9.0"],
    setup_requires=["nose"],
    tests_require=["nose", "tox"],
    url="http://www.scalr.com"
)
