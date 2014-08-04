import sys

from setuptools import setup, find_packages

setup(
    name='ConwayCPU',
    version='0.5',
    description="The Game of Life, living on your CPU",
    long_description=open('README.txt').read(),
    author='Rupert Deese',
    author_email='hartdeese@mac.com',
    license='MIT',
    packages=find_packages(exclude=['ez_setup']),
    scripts=['bin/ConwayCPU.py'],
    url='http://pypi.python.org/pypi/ConwayCPU/',
    include_package_data=True,
    install_requires=[
        'blessings>=1.5,<2.0',
        'psutil >=2.1'
    ],
    classifiers=[
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Topic :: Artistic Software',
        'Topic :: Games/Entertainment :: Simulation',
        'Topic :: Scientific/Engineering :: Artificial Life',
        'Topic :: Terminals'
        ],
    keywords=['terminal', 'tty', 'console', 'game', 'life']
)
