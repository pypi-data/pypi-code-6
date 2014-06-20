from distutils.core import setup

setup(
    name='abacus',
    version='0.1.1',
    author='Rit Li',
    author_email='rit@quietdynamite.com',
    packages=['abacus', 'abacus.test'],
    url='https://bitbucket.org/rit/abacus',
    license='http://opensource.org/licenses/MIT',
    description='Helper Library for Tornado Web Framework',
    long_description=open('README.rst').read(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
)
