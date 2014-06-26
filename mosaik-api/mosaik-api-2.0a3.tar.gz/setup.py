from setuptools import setup, find_packages


setup(
    name='mosaik-api',
    version='2.0a3',
    author='Stefan Scherfke',
    author_email='stefan.scherfke at offis.de',
    description='Python implementation of the mosaik API.',
    long_description='\n\n'.join(
        open(f, 'rb').read().decode('utf-8')
        for f in ['README.txt', 'CHANGES.txt', 'AUTHORS.txt']),
    url='https://mosaik.offis.de',
    install_requires=[
        'docopt>=0.6.1',
        'simpy>=3.0.5',
        'simpy.io>=0.2',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pyexamplemas = example_mas.mosaik:main',
            'pyexamplesim = example_sim.mosaik:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
