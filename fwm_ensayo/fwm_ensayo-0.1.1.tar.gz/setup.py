#!/usr/bin/env python
import os
from numpy.distutils.core import setup, Extension

ext1=Extension(name='mode',sources=['fwm_ensayo/cuencas.f90','fwm_ensayo/lluvia.f90','fwm_ensayo/modelos.f90',])

setup(
    name='fwm_ensayo',
    version='0.1.1',
    author='Nicolas Velasquez G',
    author_email='nicolas.velasquezgiron@gmail.com',
    ext_modules=[ext1],
    packages=['fwm_ensayo'],
    #package_data={'fwm_ensayo':['modelacion']},
    url='http://pypi.python.org/pypi/fwm_ensayo/',
    license='LICENSE.txt',
    description='.',
    long_description=open('README.txt').read(),
)
