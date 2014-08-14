from setuptools import setup
from distutils.core import Extension
from Cython.Distutils import build_ext
from os.path import join, dirname
import numpy as np

ext_mbar = Extension(
        "pyfeat.estimator.mbar.ext",
        sources=["ext/mbar/mbar.pyx", "ext/mbar/_mbar.c" ],
        include_dirs=[np.get_include()],
        extra_compile_args=["-O3"]
    )

def read( filename ):
    return open( join( dirname( __file__ ), filename ) ).read()

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[ ext_mbar ],
    name='pyfeat',
    version='0.2.3',
    description='The python free energy analysis toolkit',
    long_description=read( 'README.rst' ),
    classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: C',
            'Programming Language :: Cython',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            'Topic :: Scientific/Engineering :: Chemistry',
            'Topic :: Scientific/Engineering :: Mathematics',
            'Topic :: Scientific/Engineering :: Physics'
        ],
    keywords=[ 'MBAR', 'WHAM', 'free energy' ],
    url='http://github.com/cmb-fu/pyfeat',
    author='The pyfeat team',
    author_email='pyfeat@lists.fu-berlin.de',
    license='Simplified BSD License',
    setup_requires=[ 'numpy>=1.7.1', 'cython>=0.15', 'setuptools>=0.6' ],
    tests_require=[ 'numpy>=1.7.1' ],
    install_requires=[ 'numpy>=1.7.1' ],
    packages=[
            'pyfeat',
            'pyfeat.data',
            'pyfeat.reader',
            'pyfeat.estimator',
            'pyfeat.estimator.mbar',
            'pyfeat.estimator.wham',
            'pyfeat.exception',
        ],
    scripts=[
            'bin/run_mbar.py',
            'bin/run_wham.py'
        ]
)
