from setuptools import setup


setup(
    name='mosaik-hdf5',
    version='0.2',
    author='Stefan Scherfke',
    author_email='stefan.scherfke at offis.de',
    description=('Stores mosaik simulation data in an HDF5 database.'),
    long_description=(open('README.txt').read() + '\n\n' +
                      open('CHANGES.txt').read() + '\n\n' +
                      open('AUTHORS.txt').read()),
    url='https://bitbucket.org/mosaik/mosaik-hdf5',
    install_requires=[
        'h5py>=2.2.1',
        'mosaik-api>=2.1',
        'networkx>=1.9',
        'numpy>=1.8.1',
    ],
    py_modules=['mosaik_hdf5'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mosaik-hdf5 = mosaik_hdf5:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
    ],
)
