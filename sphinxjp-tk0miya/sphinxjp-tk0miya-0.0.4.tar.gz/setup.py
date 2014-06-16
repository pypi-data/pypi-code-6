# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = open("README.rst").read()

requires = ['Sphinx>=0.6', 'setuptools', 'flickr_api']

setup(
    name='sphinxjp-tk0miya',
    version='0.0.4',
    url='http://bitbucket.org/r_rudi/sphinxjp.tk0miya',
    download_url='http://pypi.python.org/pypi/sphinxjp-tk0miya',
    license='BSD',
    author='WAKAYAMA Shirou',
    author_email='shirou.faw@gmail.com',
    description='Sphinx flicker API extention',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxjp'],
)
