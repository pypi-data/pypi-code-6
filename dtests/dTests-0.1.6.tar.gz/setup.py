from distutils.core import setup
version = '0.1.6'
setup(
    name='dTests',
    version=version,
    author='Mohamed Bassem',
    author_email='medoox240@gmail.com',
    packages=['dTests', 'dTests.server', 'dTests.node', 'dTests.utils'],
    scripts=['bin/dtests_node','bin/dtests_server','bin/dtests_job'],
    license='LICENSE.txt',
    description='A python tool to distributively run GCJ/FB hacker cup testcases on several machines.',
    keywords=['GCJ', 'tests', 'distributed'],
    url = 'https://github.com/MohamedBassem/dTests',
    long_description=open('README.txt').read(),
)
