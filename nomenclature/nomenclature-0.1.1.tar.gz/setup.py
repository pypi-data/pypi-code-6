from setuptools import setup

import versioneer
versioneer.versionfile_source = 'nomenclature/_version.py'
versioneer.versionfile_build = 'nomenclature/_version.py'
versioneer.tag_prefix = 'v'
versioneer.parentdir_prefix = 'nomenclature-'


def read(path):
    """
    Read the contents of a file.
    """
    with open(path) as f:
        return f.read()

try:
    from nomenclature import _lib
except ImportError:
    # installing - there is no cffi yet
    ext_modules = []
else:
    # building bdist - cffi is here!
    ext_modules = [_lib.ffi.verifier.get_extension()]

setup(
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    name='nomenclature',
    version=versioneer.get_version(),
    description="Linux Namespace Manipulation",
    install_requires=["cffi"],
    license="APL2",
    packages=["nomenclature", "nomenclature.tests"],
    url="https://github.com/hybridcluster/nomenclautre/",
    maintainer='Tom Prince',
    maintainer_email='tom.prince@hybridcluster.com',
    long_description=read('README.rst'),
    cmdclass=versioneer.get_cmdclass(),

    package_data={
        'nomenclature': ['c/*.h'],
    },

    ext_package="nomenclature",
    ext_modules=ext_modules,
)
