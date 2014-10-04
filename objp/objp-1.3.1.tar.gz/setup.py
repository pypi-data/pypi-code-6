from setuptools import setup

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
]

LONG_DESC = open('README.rst', 'rt').read() + '\n\n' + open('CHANGES.rst', 'rt').read()

setup(
    name='objp',
    version='1.3.1',
    author='Hardcoded Software',
    author_email='hsoft@hardcoded.net',
    packages=['objp'],
    package_data={'objp': ['data/*']},
    scripts=[],
    install_requires=[],
    url='https://github.com/hsoft/objp',
    license='BSD License',
    description='Python<-->Objective-C bridge with a code generation approach',
    long_description=LONG_DESC,
    classifiers=CLASSIFIERS,
)
