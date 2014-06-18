import os
from setuptools import setup, find_packages

install_requires = ["jinja2==2.5", "tornado", "requests", "pyyaml", "six", "u-msgpack-python"]

base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name="stagecoach-apy",
    version="1.1.2",
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
