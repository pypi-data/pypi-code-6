from setuptools import setup, find_packages
import os

version = '1.1.0'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('js', 'url_parser', 'test_url-parser.txt')
    + '\n' +
    read('CHANGES.txt'))

setup(
    name='js.url_parser',
    version=version,
    description="Fanstatic packaging of url-parser",
    long_description=long_description,
    classifiers=[],
    keywords='fanstatic js javascript url parser',
    author='Denis Sukhonin',
    url='https://bitbucket.org/negval/js.url_parser',
    author_email='d.sukhonin@gmail.com',
    license='BSD',
    packages=find_packages(), namespace_packages=['js'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'fanstatic',
        'setuptools',
    ],
    entry_points={
        'fanstatic.libraries': [
            'url-parser = js.url_parser:library',
        ],
    },
)
