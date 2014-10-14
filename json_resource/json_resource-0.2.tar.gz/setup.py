from setuptools import setup
from setuptools_behave import behave_test

__VERSION__ = '0.2'

setup(
    name='json_resource',
    version=__VERSION__,
    packages=['json_resource'],
    long_description=open('./README.rst').read(),
    author='Ernst Odolphi',
    author_email='ernst.odolphi@gmail.com',
    install_requires=['json_pointer', 'jsonschema', 'json_patch', 'pymongo'],
    tests_require=['behave'],
    cmdclass={"behave_test": behave_test}
)




