PROJECT = 'crepopy'

# Change docs/sphinx/conf.py too!
VERSION = '0.0.1'

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description=PROJECT,
    long_description=long_description,

    author='jamesbeedy',
    author_email='jamesbeedy@gmail.com',

    url='https://github.com/jamesbeedy/crepopy',
    download_url='https://github.com/jamesbeedy/crepopy',


    # 1.2.0.dev1  # Development release
    # 1.2.0 a1     # Alpha Release
    # 1.2.0b1     # Beta Release
    # 1.2.0rc1    # RC Release
    # 1.2.0       # Final Release
    # 1.2.0.post1 # Post Release

    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Topic :: Software Development :: Build Tools',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    keywords='sample setuptools development',

    platforms=['Any'],
    scripts=[],
    provides=[],
    install_requires=['cliff'],
    namespace_packages=[],
    packages=find_packages(exclude=['']),
    include_package_data=True,

    entry_points={
        'console_scripts':[
            'crepopy = crepopy.main:main'
        ],
        'crepopy.app':[
            'create = crepo.create:Create',
            'listrepos = crepo.list_repos:ListRepos'
        ],
    },
)