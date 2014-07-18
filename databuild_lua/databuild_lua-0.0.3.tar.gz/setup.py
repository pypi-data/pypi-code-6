import os
from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

VERSION = "0.0.3"


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
            return fh.read()
    except IOError:
        return ''

requirements = read('requirements.txt').splitlines()

pypi_requirements = [req for req in requirements if not req.startswith('http')]
dependency_links = [req for req in requirements if req.startswith('http')]

tests_requirements = read('test-requirements.txt').splitlines()


class InstallLupa(install):
    def run(self):
        # Temporary fix until lupa gets released
        install.run(self)
        subprocess.check_call(["pip", "install", "--quiet", "https://github.com/scoder/lupa/archive/master.tar.gz"], cwd=self.install_lib)


setup(
    name="databuild_lua",
    version=VERSION,
    description="Lua Environment Plugin for Databuild",
    long_description=read('README.rst'),
    url='https://github.com/databuild/databuild-lua',
    license='BSD',
    author='Flavio Curella',
    author_email='flavio.curella@gmail.com',
    packages=find_packages(exclude=['tests']),
    cmdclass={"install": InstallLupa},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    install_requires=pypi_requirements,
    dependency_links=dependency_links,
    tests_require=tests_requirements,
)
