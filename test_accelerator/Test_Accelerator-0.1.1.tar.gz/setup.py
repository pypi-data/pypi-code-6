__author__ = 'root'

from setuptools import setup

setup(
    name='Test_Accelerator',
    version='0.1.1',
    author='Tanner Baldus',
    url='https://github.com/TannerBaldus/test_accelerator',
    author_email='tbaldus@electric-cloud.com',
    packages=['src'],
    scripts=[],
    description='Extracts unit test names from source files to GNU makefiles\
                so you can speed use emake to run your tests',
    entry_points={
        'console_scripts': [
         'ecconvert = src.converter:main',
         'ecparse = src.parser:main'
        ],
        }
)
