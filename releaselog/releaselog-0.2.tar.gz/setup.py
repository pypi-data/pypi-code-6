from setuptools import setup
from setuptools import find_packages

from releaselog import __version__

setup(
    name='releaselog',
    version=__version__,
    author='Mike Ruckman',
    author_email='roshi@fedorapeople.org',
    url='https://www.bitbucket.org/Rorosha/releaselog/',

    # Descriptions
    description='Generate release notess from git commit logs.',

    packages=['releaselog'],
    entry_points = {
        'console_scripts': [
            'releaselog=releaselog:main',
        ],
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 2.7',
    ]
)
