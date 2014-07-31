from distutils.core import setup

setup(
    name='dTests',
    version='0.1.4',
    author='Mohamed Bassem',
    author_email='medoox240@gmail.com',
    packages=['dTests', 'dTests.server', 'dTests.node', 'dTests.utils'],
    scripts=['bin/dtests_node','bin/dtests_server','bin/dtests_job'],
    url='http://pypi.python.org/pypi/dTests/',
    license='LICENSE.txt',
    description='A python tool to distributively run GCJ/FB hacker cup testcases on several machines.',
    long_description=open('README.txt').read(),
)
