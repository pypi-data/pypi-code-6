import re
import ast
from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')


with open('NIWLittleUtils/__init__.py', 'rb') as f:
    version = ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1))

with open('README.rst', 'rb') as f:
    long_description = f.read().decode('utf-8')

setup(
    name='NIWLittleUtils',
    author='NIWyclin (a.k.a. birdhackor)',
    author_email='NIWLittleUtils@mymail.niwyclin.org',
    license='LGPLv3',
    version=version,
    url='https://bitbucket.org/birdhackor/niwlittleutils',
    packages=['NIWLittleUtils'],
    description='NIWLittleUtils is a tool collection.',
    long_description=long_description,
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
