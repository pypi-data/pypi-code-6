from setuptools import setup, find_packages

#next time:
#python setup.py register
#python setup.py sdist upload

version = open('ironeagle/VERSION', 'r').readline().strip()

long_desc = """

"""

setup(
    name='ironeagle',
    version=version,
    description='Helper library for working with Pandas and the Cassandra Native Driver',
    long_description=long_desc,
    classifiers = [
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        
    ],
    keywords='cassandra,cql,pandas',
    install_requires = ['cassandra-driver >= 2.1.0', 'pandas >= 0.15.0'],
    author='Jon Haddad',
    author_email='jon@jonhaddad.com',
    url='https://github.com/rustyrazorblade/ironeagle',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
)
