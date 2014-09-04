#!/usr/bin/env python

from setuptools import setup, find_packages

# Copied from: https://github.com/rg3/youtube-dl/blob/master/setup.py
exec(compile(open('jms_utils/version.py').read(),
             'jms_utils/version.py', 'exec'))

setup(
    name='JMS-Utils',
    version=__version__,
    description='Various utility functions',
    author='Johny Mo Swag',
    author_email='johnymoswag@gmail.com',
    url='https://github.com/JohnyMoSwag/jms-utils',
    download_url=('https://github.com/JohnyMoSwag/jms'
                  '-utils/archive/master.zip'),
    license='MIT',
    install_requires=[
        ],
    packages=find_packages(),
    # package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'],
    )
