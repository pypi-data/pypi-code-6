import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
import os

name = "watchit"
version = "0.0.1"

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name=name,
    version=version,
    author='Jake Hickenlooper',
    author_email='jake@weboftomorrow.com',
    description="Watch a directory for file changes and exit",
    long_description=read('README.rst'),
    url="https://github.com/jkenlooper/watchit",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Topic :: Software Development :: Build Tools',
        ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'watchdog',
        'docopt',
      ],
    entry_points={
        'console_scripts': [
            'watchit = watchit.script:main',
            ]
        },
)
