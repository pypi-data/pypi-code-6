try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='ENCODEQueryTools',
    version='0.1.0',
    author='Raymond Auerbach',
    author_email='rauerbac@stanford.edu',
    packages=['ENCODEQueryTools'],
    url='https://bitbucket.org/rauerbach/encodequerytools',
    download_url="https://bitbucket.org/rauerbach/encodequerytools/downloads/ENCODEQueryTools-0.1.0.tar.gz",
    license='LICENSE.txt',
    description='Module to query ENCODE ChIP-Seq TF Significance Tool (http://encodeqt.stanford.edu) using API calls.',
    long_description=open('README.rst').read(),
    install_requires=[
        'pandas>=0.14.0',
    ],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
)
