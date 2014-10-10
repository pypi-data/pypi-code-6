from setuptools import setup
import pkg_resources
import re


def read(path):
    with open(pkg_resources.resource_filename(__name__, path)) as f:
        return f.read()


def long_description():
    return re.split('\n\.\. pypi [^\n]*\n', read('README.rst'), 1)[1]


setup(
    name='refund_calculation',
    version='0.1',
    author='Chris Martin',
    author_email='ch.martin@gmail.com',
    packages=['refund_calculation'],
    url='https://github.com/chris-martin/refund-calculation',
    license='MIT',
    description=
        'Turns a chronological sequence of balance-adjustment events into '
        'a timeline of periods during which particular balances were held.',
    long_description=long_description(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=read('requirements-install.txt').split('\n'),
    tests_require=read('requirements-test.txt').split('\n'),
)
