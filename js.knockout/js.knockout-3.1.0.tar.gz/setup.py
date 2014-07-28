from setuptools import setup, find_packages
import os

# The version of the wrapped library is the starting point for the
# version number of the python package.
# In bugfix releases of the python package, add a '-' suffix and an
# incrementing integer.
# For example, a packaging bugfix release version 1.4.4 of the
# js.jquery package would be version 1.4.4-1 .

version = '3.1.0'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('js', 'knockout', 'test_knockout.txt')
    + '\n' +
    read('CHANGES.txt'))

extras_require = {
    'test': [],
    }

setup(
    name='js.knockout',
    version=version,
    description="Fanstatic packaging of Knockout",
    long_description=long_description,
    classifiers=[],
    keywords='',
    author='gocept Developers',
    author_email='mail@gocept.com',
    license='BSD',
    packages=find_packages(),namespace_packages=['js'],
    include_package_data=True,
    url='https://bitbucket.org/gocept/js.knockout',
    zip_safe=False,
    install_requires=[
        'fanstatic',
        'setuptools',
        ],
    extras_require=extras_require,
    entry_points={
        'fanstatic.libraries': [
            'knockout = js.knockout:library',
            ],
        },
    )
