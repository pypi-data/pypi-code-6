from setuptools import setup, find_packages

VERSION = '0.1.0'

LONG_DESCRIPTION = open('README.rst').read()

setup(
    name='dynamictop',
    version=VERSION,
    description="Tools for creating a dynamic top file",
    long_description=LONG_DESCRIPTION,
    keywords='',
    author='Reuven V. Gonzales',
    author_email='reuven@virtru.com',
    url="https://github.com/virtru/dynamictop",
    license='MIT',
    platforms='*nix',
    py_modules=['dynamictop'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pyyaml==3.11',
    ],
    entry_points={},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Build Tools',
    ],
)
