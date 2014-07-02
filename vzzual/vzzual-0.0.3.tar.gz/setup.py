
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'vzzual'))
from version import VERSION

long_description = '''
The Vzzual API is designed to allow web and app developers to incorporate image
and video analysis into their applications my off-loading processing to Vzzual.

This is the official python client that wraps the Vzzual REST-like API
(http://www.vzzual.com/page_API.html).
'''

setup(
    name='vzzual',
    url="https://github.com/vzzual/vzzual-python",
    packages=['vzzual'],
    version=VERSION,
    description='Official python wrapper for the Vzzual API',
    author='Vzzual',
    author_email='support@vzzual.com',
    license='MIT License',
    install_requires=[
        'requests>=2.2.1',
        'python-dateutil',
        'simplejson',
        'nose2>=0.4.7',
        'httpretty>=0.8.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    long_description=long_description
)
