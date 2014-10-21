from setuptools import setup

setup(
    version='0.1',
    name = "sfs_upload",
    packages = ['sfs_upload'],
    description='Upload files to SFS: https://github.com/the-louie/simple-file-sharer',
    author='Jakob Hedman',
    author_email='jakob@hedman.email',
    maintainer='Jakob Hedman',
    maintainer_email='jakob@hedman.email',
    license='GNU GPLv3',
    url='https://github.com/spillevink/sfs_upload',
    package_dir = {'sfs_upload':'sfs_upload'},
    install_requires = [
        'requests',
    ],
    long_description = open('README.rst').read(),
)
