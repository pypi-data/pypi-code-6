from setuptools import setup, find_packages
import os
import os.path

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
version = open(os.path.join(here, 'version.txt')).read().strip()


setup(name='restarter',
    version=version,
    description="Automatic service restart after updates",
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    author='Christian Kauhaus',
    author_email='kc@gocept.com',
    url='https://bitbucket.org/flyingcircus/restarter',
    license='ZPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts':
            ['restarter=restarter:main']
    },
    tests_require=['mock'],
    test_suite='restarter'
)
