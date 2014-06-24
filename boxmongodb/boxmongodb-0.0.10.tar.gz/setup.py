from setuptools import setup, find_packages

setup(
    name = 'boxmongodb',
    version = '0.0.10',
    keywords = ('mongodb', 'db'),
    description = 'just a simple mongodb orm',
    license = 'MIT License',
    author = 'CcdjhMarx',
    install_requires=["pymongo>=2.7.1","bson>=0.3.3"],
    author_email = 'ccdjh.marx@all.com',
    packages = ['boxmongodb'],
)
