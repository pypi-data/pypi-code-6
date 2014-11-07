PROJECT = 'hand_evaluator'

# Change docs/sphinx/conf.py too!
VERSION = '0.0.1a'

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

    url='git.darkhorse.com/jbeedy/hand_evaluator',
    download_url='https://github.com/jamesbeedy/hand_evaluator',


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
        'console_scripts': [
            'hand_evaluator = evaluator.main:main'
        ],
        'evaluator.app': [
            'evaluate = evaluator.evaluator:Evaluate',
        ],
    },
)