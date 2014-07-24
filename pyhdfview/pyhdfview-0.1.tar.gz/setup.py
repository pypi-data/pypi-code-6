from setuptools import setup, find_packages


setup(
    name='pyhdfview',
    version=0.1,
    author='Stefan Scherfke',
    author_email='stefan at sofa-rockers.org',
    description=('A viewer for HDF5 files'),
    long_description=(open('README.txt').read() + '\n\n' +
                      open('CHANGES.txt').read() + '\n\n' +
                      open('AUTHORS.txt').read()),
    url='https://bitbucket.org/ssc/pyhdfview',
    install_requires=[
        'docopt>=0.6.2',
        'h5py>=2.3.1',
        'numpy>=1.8.1',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'hv = pyhdfview.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
    ],
)
