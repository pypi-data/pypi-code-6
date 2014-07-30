from distutils.core import setup

setup(
    name='dTests',
    version='0.1.3',
    author='Mohamed Bassem',
    author_email='medoox240@gmail.com',
    packages=['dTests', 'dTests.server', 'dTests.node', 'dTests.utils'],
    scripts=['bin/dtests_node.py','bin/dtests_server.py','bin/dtests_job.py'],
    url='http://pypi.python.org/pypi/dTests/',
    license='LICENSE.md',
    description='A python tool to distributively run GCJ/FB hacker cup testcases on several machines.',
    long_description=open('README.md').read(),
)
