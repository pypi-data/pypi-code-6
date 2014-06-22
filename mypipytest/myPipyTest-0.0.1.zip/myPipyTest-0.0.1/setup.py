#coding:utf-8

from setuptools import setup,find_packages

setup(
    name='myPipyTest',
    version='0.0.1',
    url='http://www.osforce.cn',
    license='MIT',
    author='markshao',
    author_email='xiaosj2006@126.com',
    description='a distributed test framework',
    classifiers=[
        "Programming Language :: Python",
    ],
    platforms='any',
    keywords='framework nose testing',
    packages=find_packages(exclude=['test']),
    install_requires=[
        "tox"
    ]
)