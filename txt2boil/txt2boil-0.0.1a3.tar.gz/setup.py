#!/usr/bin/python

from distutils.core import setup

with open('README.txt') as f:
    long_description = f.read()

setup(
    name='txt2boil', license='MIT', version='0.0.1a3',

    description='A configurable boilerplate generator.',
    long_description=long_description,

    author='Kieran Colford', author_email='colfordk@gmail.com',
    maintainer='Kieran Colford', maintainer_email='colfordk@gmail.com',

    url='https://github.com/kcolford/bp',
    download_url='',            # TODO

    packages=['boil', 'boil.core'],
    scripts=['txt2boil'],

    platforms=['Any'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
