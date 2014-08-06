import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'montepylib',
    version = '0.0.3',
    packages = ['montepylib', 'montepylib.tests'], #find_packages(exclude=['examples']),
    include_package_data = True,
    license = 'BSD LICENSE',
    description = 'Tools and examples to analyse high-impact business decisions, and dodge many of the problems of using spreadsheets',
    long_description = open('README.md', 'rt').read(),
    keywords = "business, cashflows, analysis, decision, spreadsheet, monte carlo, finance, corporate",
    url = 'https://bitbucket.org/artstr/montepylib',
    author = 'Arthur Street',
    author_email = 'arthur@artana.com.au',
    install_requires=[
        "pandas >= 0.13.1",
    ],
)
