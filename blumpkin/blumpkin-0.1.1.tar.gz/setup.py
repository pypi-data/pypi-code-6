import re
import setuptools


version = (
    re
    .compile(r".*__version__ = '(.*?)'", re.S)
    .match(open('blumpkin/__init__.py').read())
    .group(1)
)

packages = setuptools.find_packages('.', exclude=('tests', 'tests.*'))

install_requires = [
    'coverage',
    'nose >= 1.3.0, < 2.0',
    'nosexcover==1.0.10',
    'nose-cov==1.6',
    'nose_xunitmp==0.3.1',
    'pep8',
    'pylint',
    'pyflakes',
    'lxml'
]

extras_require = {
    'ops': [
        'fabric >=1.8,<2.0',
        'pexpect >=3.2,<4.0',
    ],
    'tests': [
        'nose >=1.0,<2.0',
        'mock >=1.0,<2.0',
        'coverage',
        'jsonschema >=2.3,<3.0',
        'moto >= 0.3, < 0.4'
    ],
}

scripts = [
    'bin/create-pypi',
]

setuptools.setup(
    name='blumpkin',
    version=version,
    url='https://github.com/balanced/blumpkin',
    author='Balanced',
    author_email='dev+blumpkin@balancedpayments.com',
    description='Testing tooling',
    platforms='any',
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=extras_require['tests'],
    packages=packages,
    scripts=scripts,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='nose.collector',
    # dependency_links=[
    #     'http://github.com/balanced/cov-core/.git#egg=cov-core'
    # ]
)
