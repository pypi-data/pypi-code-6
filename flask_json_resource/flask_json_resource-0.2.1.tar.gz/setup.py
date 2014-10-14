from setuptools import setup
from setuptools_behave import behave_test


__VERSION__ = '0.2.1'

setup(
    name='flask_json_resource',
    version=__VERSION__,
    packages=['flask_json_resource'],
    long_description=open('./README.rst').read(),
    author='Ernst Odolphi',
    author_email='ernst.odolphi@gmail.com',
    install_requires=['flask', 'json_resource', 'flask-pymongo'],
    tests_require=['behave', 'ensure'],
    cmdclass={"behave_test": behave_test}
)




