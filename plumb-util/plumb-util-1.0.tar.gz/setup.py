from setuptools import setup, find_packages

setup(
    name="plumb-util",
    version = '1.0',
    maintainer='Luminoso Technologies, Inc.',
    maintainer_email='dev@luminoso.com',
    license = "MIT",
    url = 'http://github.com/LuminosoInsight/plumb_util',
    platforms = ["any"],
    description = "Plumbing utility library",
    packages=find_packages(),
    install_requires=[
        'dnspython3',
        'pymongo',
    ],
)
