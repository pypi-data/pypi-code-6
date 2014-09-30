from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from os import path

setup(
    name='namemapping',

    version='0.1.0.dev1',

    description='A Python project uses Yahoo BOSS API to unify company names',

    url='https://github.com/biwa7636/namemapping',

    author='Bin Wang & Daniel Sweeney',
    author_email='binwang.cu@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='yahoo api boss oauth2',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['oauth2'],

    entry_points={
        'console_scripts': [
            'namemapping=namemapping:main',
        ],
    },
)
