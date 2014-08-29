# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='PyMeteostation',
    version='0.1.0',
    author='Lukáš Mičan',
    author_email='micek.luki@seznam.cz',
    url='https://github.com/MLAB-project/PyMeteostation',
    packages=['pymeteostation'],
    scripts=['bin/pymeteostation'],
    license='GNU General Public License v3 (GPLv3)',
    description='Software made for controlling meteostation built of MLAB electronic modules.',
    long_description=open('README.txt').read(),
    install_requires=['pymlab >= 0.2'],
    keywords=['meteostation','MLAB','IIC','USB'],
    classifiers=["Programming Language :: Python",
                 "Programming Language :: Python :: 2.7",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                 "Development Status :: 3 - Alpha",
                 "Intended Audience :: Science/Research"]
)
