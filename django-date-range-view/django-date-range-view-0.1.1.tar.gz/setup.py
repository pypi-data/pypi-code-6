from setuptools import setup, find_packages

setup(
    name='django-date-range-view',
    version='0.1.1',
    author='John Leith',
    author_email='leith.john@gmail.com',
    packages=find_packages(),
    license="BSD License",
    url='https://bitbucket.org/freakypie/django-date-range-view',
    description='provides a simple date range parsing django view',
    install_requires=[
        "python-dateutil"
    ],
    include_package_data=True
)
