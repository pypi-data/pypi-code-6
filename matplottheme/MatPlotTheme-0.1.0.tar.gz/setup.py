import sys

from setuptools import setup
from setuptools import find_packages

from matplottheme import __full_version__

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='MatPlotTheme',
    version=__full_version__,
    author='James Yu',
    author_email='jqyu@eee.hku.hk',
    description='MatPlotTheme is a theming library for MatPlotLib.',
    long_description=long_description,
    url="https://github.com/James-Yu/MatPlotTheme",

    install_requires=['matplotlib'],

    packages=find_packages(),
    package_data={'matplottheme': ['tests/baseline_images/*/*.png']},

    license='MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering'
    ],
)
