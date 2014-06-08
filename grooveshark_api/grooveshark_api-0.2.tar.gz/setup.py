#!/usr/bin/env python


from distutils.core import setup
setup(
    name='grooveshark_api',
    version='0.2',
    description='A Wrapper to the Grooveshark API V3',
    long_description="",
    keywords=['api', 'grooveshark', 'streaming', 'audio'],
    author='Rafael Soares',
    author_email='rafaeltravel88@gmail.com',
    url='http://github.com/rafaels88/grooveshark-api',
    license='MIT',
    packages=['grooveshark_api'],
    include_package_data=True,
    install_requires=['requests==2.2.1']
)
