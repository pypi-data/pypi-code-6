#!/usr/bin/python
#coding:utf8


from setuptools import setup,find_packages

setup(
    name="Dell_RaidMonitor",
    version="0.0.1",
    author="Boyle Gu",
    author_email="gubaoer@hotmail.com",
    license="BSD",
    url="www.51cto.com",
    description="Monitor Dell Raid",
    classifiers=[
		"Programming Language :: Python",
		],
    platforms="any",
    packages=find_packages(exclude=["tests"]),
	  )
