import re
import setuptools


setuptools.setup(
    name='coid',
    version=(
        re
        .compile(r".*__version__ = '(.*?)'", re.S)
        .match(open('coid.py').read())
        .group(1)
    ),
    url='https://github.com/bninja/coid',
    license='BSD',
    author='stu',
    author_email='stu@unger.rummy',
    description='Id codecs.',
    long_description=open('README.rst').read(),
    py_modules=['coid'],
    include_package_data=True,
    platforms='any',
    install_requires=[
    ],
    extras_require={
        'tests': [
            'pytest >=2.5.2,<3',
            'pytest-cov >=1.7,<2',
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
