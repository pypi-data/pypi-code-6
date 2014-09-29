'''

@author: Administrator

CellMethy_v1

This script is used for infering fraction of focal full methylation cell subpopulation.

Easy to start: 
Inputfile: File sepearated by "\t" after bismark processed including read id, strand, chromosome, position of CpGc and methylation state (Z or z)
The result would be placed into input folder: CellMethy.out

Options:
"-f","--infilename",dest="infilename",type="str",help="The file name of input file after bismark processed, include five columns: read ID, strand, chromosome, position of CpG and methylation states Z (methylated) or z (unmethylated) separated by \t")
"-b","--BinLength",dest="BinLength",type="int",default="5",help="number of CpGs in each bin, default is 5")
"-c","--coverage_cutoff",dest="coverage_cutoff",type="int",default="10",help="Lowest coverage cutoff in each bin, default is 10")
"-o","--outfilename",dest="outfilename",type="str",default="CellMethy.out",help="The file name of output file showing full methylation of cell subpopulation, include five columns: chromosome, start, end, 3CellMethy, and CpGs number in the region separated by \t")

 

'''

from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CellMethy',
    version='1.1.27',

    description='Identifying focal full methylation of cell subpopulation and inferring fraction',
    long_description=long_description,
    scripts = ['CellMethy/bin/CellMethy.py'],
    # The project's main homepage.
    url='https://github.com/pypa/CellMethyproject',

    # Author details
    author='Fang Wang',
    author_email='wangfang@ems.hrbmu.edu.cn',

    # Choose your license
    license='Harbin Medical University, Python Software Foundation License',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Operating System :: POSIX',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='CellMethy setuptools development',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),
  
)
