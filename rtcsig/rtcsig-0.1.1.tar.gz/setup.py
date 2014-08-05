import os
from setuptools import setup


def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='rtcsig',
    version='0.1.1',
    url='https://github.com/maurostorch/rtcsig',

    description='This is a Django App for handle the session exchanging of a WebRTC peer interconnection',
    long_description=read('README.md'),
    license='The MIT License (MIT)',

    author='Mauro Storch',
    author_email='mauro@storchlab.com',

    packages=['rtcsig'],
    include_package_data=True,
    zip_safe=False,

    install_requires=['django-etc'],

    classifiers=[
        # As in https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Topic :: Communications',
        'Topic :: Communications :: File Sharing'
    ],
)

