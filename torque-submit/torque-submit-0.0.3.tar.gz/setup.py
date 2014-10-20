
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='torque-submit',
    version='0.0.3',
    packages=['torqsubmit'],
    url='https://github.com/jbzdak/torque-submitter',
    license='Apache 2.0',
    author='Jacek Bzdak',
    author_email='jbzdak@gmail.com',
    description='Python script to submit torque jobs in a very hackish way',
    classifiers="""
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: Apache Software License
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.4
    """.strip().split('\n')
)
