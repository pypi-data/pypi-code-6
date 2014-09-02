from setuptools import setup, find_packages
import os

version = '1.0.1'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('js', 'q', 'test_q.txt')
    + '\n' +
    read('CHANGES.txt'))

setup(
    name='js.q',
    version=version,
    description="Fanstatic packaging of q",
    long_description=long_description,
    classifiers=[],
    keywords='fanstatic js javascript q',
    author='Denis Sukhonin',
    url='https://bitbucket.org/negval/js.q',
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
            'q = js.q:library',
        ],
    },
)
