import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pypiece",
    version = "0.1.3",
    author = "Kirill Borisov",
    author_email = "lensvol@gmail.com",
    description = ("Wrapper around pip for flakey connections."),
    license = "MIT",
    keywords = "pip",
    url = "https://github.com/lensvol/pypiece",
    packages=['pypiece'],
    long_description=read('README.md'),
    install_requires=["click>=2.4"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
        'console_scripts': [
            'pypiece = pypiece.pypiece:piecemeal_install'
        ]
    }
)
