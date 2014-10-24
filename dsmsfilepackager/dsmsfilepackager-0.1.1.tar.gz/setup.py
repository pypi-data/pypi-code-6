from setuptools import setup

setup(
    name='dsmsfilepackager',
    version='0.1.1',
    author='Chris Horsley',
    author_email='chris.horsley@csirtfoundry.com',
    packages=['dsmsfilepackager'],
    scripts=[],
    url='http://bitbucket.org/dsms/dsmsfilepackager/',
    license='LICENSE.txt',
    description='',
    long_description=open('README').read(),
    install_requires=[
        "sftpsyncer",
        "python-magic"
    ],
)
