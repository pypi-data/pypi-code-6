from pip.req import parse_requirements
from setuptools import setup, find_packages

from helga_mud import __version__ as version

requirements = [
    str(req.req) for req in parse_requirements('requirements.txt')
]


setup(
    name='helga-mud',
    version=version,
    description=(''),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat :: Internet Relay Chat'],
    keywords='irc bot mud',
    author='Michael Orr',
    author_email='michael@orr.co',
    url='https://github.com/michaelorr/helga-mud',
    license='LICENSE',
    packages=find_packages(),
    include_package_data=True,
    py_modules=['helga_mud.plugin'],
    zip_safe=True,
    install_requirements=requirements,
    entry_points = dict(
        helga_plugins=[
            'mud = helga_mud.plugin:mud',
        ],
    ),
)
