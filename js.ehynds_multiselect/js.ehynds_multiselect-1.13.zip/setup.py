from setuptools import setup, find_packages
import os

# The version of the wrapped library is the starting point for the
# version number of the python package.
# In bugfix releases of the python package, add a '-' suffix and an
# incrementing integer.
# For example, a packaging bugfix release version 1.4.4 of the
# js.jquery package would be version 1.4.4-1 .

version = '1.13'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('js', 'ehynds_multiselect', 'test_multiselect.txt')
    + '\n' +
    read('CHANGES.txt'))

setup(
    name='js.ehynds_multiselect',
    version=version,
    description="Fanstatic packaging of ehynds/jquery-ui-multiselect-widget",
    long_description=long_description,
    classifiers=[],
    keywords='',
    author='gocept Developers',
    author_email='mail@gocept.com',
    license='BSD',
    packages=find_packages(),namespace_packages=['js'],
    include_package_data=True,
    url='https://bitbucket.org/gocept/js.ehynds_multiselect',
    zip_safe=False,
    install_requires=[
        'fanstatic',
        'js.jquery >= 1.7.1',
        'js.jqueryui >= 1.8.0',
        'setuptools',
        ],
    entry_points={
        'fanstatic.libraries': [
            'colorpicker = js.ehynds_multiselect:library',
            ],
        },
    )
