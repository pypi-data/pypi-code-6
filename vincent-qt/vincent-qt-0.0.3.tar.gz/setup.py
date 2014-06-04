from setuptools import setup, find_packages
import codecs
import os

import vincent_qt

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="vincent-qt",
    version=vincent_qt.__version__,
    description="Vincent in QtWidgets applications",
    long_description=long_description,
    url='https://bitbucket.org/rominf/vincent-qt',
    author='Roman Inflianskas',
    author_email='infroma@gmail.com',
    license='LGPLv3+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='vincent plot chart qt',
    install_requires=['vincent', 'appdirs'],
    packages=find_packages(exclude=['tests*']),
    package_data={
        'vincent_qt': ['package_data.dat'],
    },
)
