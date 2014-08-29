from distutils.core import setup, Extension
import glob
import numpy as np
from setuptools import setup, Extension, Command

sources = ['pysofia/_sofia_ml.cpp'] + glob.glob('pysofia/src/*.cc')
headers = glob.glob('pysofia/src/*.h')

setup(name='pysofia',
    version='0.8',
    description='Python bindings for sofia-ml',
    long_description=open('README.rst').read(),
    author='Fabian Pedregosa',
    author_email='fabian@fseoane.net',
    url='http://pypi.python.org/pypi/pysofia',
    packages=['pysofia'],
    ext_modules = [Extension('_sofia_ml',
        sources=sources,
        headers=headers,
        language='c++', include_dirs=[np.get_include()])],
)
