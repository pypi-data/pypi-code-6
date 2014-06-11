'''Sahuwai setuptools'''

from setuptools import setup
from setuptools import find_packages

setup(name='sahuwai',
    version='0.1',
    description='RRDA REST DNS API client.',
    long_description=' ',
    install_requires=['setuptools','drest'],
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 2.7',
      'Topic :: Internet :: Name Service (DNS)',
    ],
    keywords=[
        'rest', 'dns', 'api',
    ],
    author='Teguh P. Alko',
    author_email='chain@rop.io',
    url='http://rtfd.rop.io/sahuwai/',
    license='BSD 3-Clause License',
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    zip_safe=False,
)
