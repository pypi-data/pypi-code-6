from distutils.core import setup

setup(
    name='OpenSprinklerLib',
    version='0.1.0',
    author='David Miller',
    author_email='david3d@gmail.com',
    packages=['opensprinklerlib', 'opensprinklerlib.controller'],
    url='http://pypi.python.org/pypi/OpenSprinklerLib/',
    license='LICENSE.txt',
    description='OpenSprinkler Library and demos.',
    long_description=open('README.md').read(),
    classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 2.7",
            "Topic :: Home Automation",
            "Topic :: Software Development",
            "Topic :: System :: Hardware",
    ],
)
