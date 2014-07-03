# coding: utf-8
import setuptools
import os

README = os.path.join(os.path.dirname(__file__), 'README.rst')
REQ = os.path.join(os.path.dirname(__file__), 'requirements.txt')

setuptools.setup(
    name='fixofx',
    version='3.0',
    description='Canonicalize various financial data file formats to OFX 2 (a.k.a XML)',
    long_description=open(README).read(),
    author='Henrique Bastos',
    author_email='henrique@bastos.net',
    url='http://github.com/henriquebastos/fixofx',
    packages=['fixofx', 'fixofx.ofx', 'fixofx.ofxtools'],
    package_data = {
        '': ['*.txt', '*.rst'],
    },
    scripts=['bin/ofxfix.py','bin/ofxfake.py'],
    install_requires=open(REQ).readlines(),
    license='Apache 2.0',
    keywords='ofx, ofc, qif, converter, xml',
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Financial and Insurance Industry',
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries',
          'Topic :: Text Processing',
    ],
)
