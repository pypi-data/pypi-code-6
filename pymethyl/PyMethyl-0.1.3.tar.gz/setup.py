##File to install pymethyl package

##Author: Cody Watson and Sandy Weng

from setuptools import setup, find_packages

setup(
    name='PyMethyl',
    version='0.1.3',
    author='Cody Watson and Sandy Weng',
    author_email='watsonca@email.wofford.edu',
    packages= find_packages(),
    package_data = {
        '':['*.txt', '*.rst']
        },
    keywords = "Methylation patterns",
    url= 'https://pypi.python.org/pypi/PyMethyl',
    license='LICENSE.txt',
    description='Tool to determine methylation patterns.',
    long_description=open('README.txt').read(),
    install_requires=[
        "cruzdb == 0.5.6",
        "sqlalchemy >= 0.7",
        "pysam >= 0.8.0",
	"MySQL-python"
    ]
)
