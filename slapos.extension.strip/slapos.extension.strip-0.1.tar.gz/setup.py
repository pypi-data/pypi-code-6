from setuptools import setup, find_packages
import os

version = '0.1'
name = 'slapos.extension.strip'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name=name,
    version=version,
    description="zc.buildout extension to strip binaries.",
    long_description=(
        read('README.rst')
        + '\n' +
        read('CHANGES.txt')
        + '\n' +
        'Download\n'
        '***********************\n'
    ),
    classifiers=[
        'Framework :: Buildout :: Extension',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Build Tools',
    ],
    keywords='buildout extension strip',
    author='Kazuhiko Shiozaki',
    author_email='kazuhiko@nexedi.com',
    url='http://git.erp5.org/gitweb/slapos.extension.strip',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['slapos', 'slapos.extension'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'zc.buildout',
    ],
    entry_points = { 
        'zc.buildout.unloadextension': [
             'default = slapos.extension.strip:finish',
             ],
        },
)
