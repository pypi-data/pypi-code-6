from setuptools import setup, find_packages

VERSION = '0.5.1'

setup(
    name='cockatoo',
    description='cockatoo - A similarity metric for macromolecular crystallization conditions',
    long_description='cockatoo is an implementation of a similarity metric used in the comparison of macromolecular crystallization conditions (or cocktails).',
    author='Andrew E. Bruno',
    url='https://github.com/ubccr/cockatoo',
    license='GNU General Public License v3 (GPLv3)',
    author_email='aebruno2@buffalo.edu',
    version=VERSION,
    include_package_data=True,
    packages=find_packages(exclude=['tests*']),
    package_data={'cockatoo': ['data/*.csv', 'data/*.json']},
    install_requires=[
        'click',
        'pinky',
        'marshmallow<=0.7.0',
    ],
    entry_points='''
        [console_scripts]
        cockatoo=cockatoo.cli:main
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
     ]
)
