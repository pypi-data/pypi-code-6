from setuptools import setup, find_packages

VERSION = '0.1.0'

LONG_DESCRIPTION = open('README.rst').read()

setup(
    name='env-render',
    version=VERSION,
    description="Generates files by parsing the environment with jinja2",
    long_description=LONG_DESCRIPTION,
    keywords='',
    author='Reuven V. Gonzales',
    author_email='reuven@virtru.com',
    url="https://github.com/virtru/env-render",
    license='MIT',
    platforms='*nix',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'jinja2==2.7.3'
    ],
    entry_points={
        'console_scripts': [
            'env-render=envrender.cli:run',
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Build Tools',
    ],
)
