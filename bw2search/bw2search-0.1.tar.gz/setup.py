from setuptools import setup


setup(
    name='bw2search',
    version="0.1",
    packages=["bw2search"],
    author="Chris Mutel",
    author_email="cmutel@gmail.com",
    license=open('LICENSE.txt').read(),
    install_requires=["bw2data"],
    url="https://bitbucket.org/cmutel/brightway2-search",
    long_description=open('README.rst').read(),
    description=('Search functionality for the Brightway2 LCA Framework'),
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],)
