import os
from setuptools import setup, find_packages


requirements_file = open('%s/requirements.txt' % os.path.dirname(os.path.realpath(__file__)), 'r')
install_requires = [line.rstrip() for line in requirements_file]
base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name="stagecoach-apy",
    version="1.1.4",
    description="Python RESTful API Framework",
    long_description="\n\n".join([
        open(os.path.join(base_dir, "README.rst"), "r").read(),
    ]),
    url="https://github.com/stagecoachio/apy",
    author="Felix Carmona",
    author_email="mail@felixcarmona.com",
    packages=find_packages(exclude=('apy.tests', 'apy.tests.*')),
    zip_safe=False,
    install_requires=install_requires,
    test_suite="apy.tests.get_tests",
)
