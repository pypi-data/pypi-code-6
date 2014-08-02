import os
from setuptools import setup, find_packages


requirements_file = open('%s/requirements.txt' % os.path.dirname(os.path.realpath(__file__)), 'r')
install_requires = [line.rstrip() for line in requirements_file]
base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name="apy-users",
    version="0.0.2",
    description="Provides user management and API authentication for your apy project",
    long_description="\n\n".join([
        open(os.path.join(base_dir, "README.rst"), "r").read(),
    ]),
    url="https://github.com/stagecoachio/apy-users",
    author="Felix Carmona",
    author_email="mail@felixcarmona.com",
    packages=find_packages(exclude=('apy_users.tests', 'apy_users.tests.*')),
    zip_safe=False,
    install_requires=install_requires,
    test_suite="apy_users.tests.get_tests",
)
