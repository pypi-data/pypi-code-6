import re
import setuptools


setuptools.setup(
    name='virtualenv-relocate',
    version=(
        re
        .compile(r".*__version__ = '(.*?)'", re.S)
        .match(open('virtualenv-relocate').read())
        .group(1)
    ),
    url='https://github.com/bninja/virtualenv-relocate',
    license='BSD',
    author='noone',
    author_email='noone@nowhere.net',
    description='https://github.com/pypa/virtualenv/issues/558',
    long_description=open('README.rst').read(),
    platforms='any',
    install_requires=[],
    extras_require={},
    tests_require=[],
    scripts=['virtualenv-relocate'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
