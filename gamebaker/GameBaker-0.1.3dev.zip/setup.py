from distutils.core import setup
from os.path import join

setup(
    name="GameBaker",
    version="0.1.3dev",
    description="High level framework for making games and simulations based on Pygame",
    packages=["gamebaker",],
    package_dir={"gamebaker": "gamebaker"},
    package_data={"gamebaker": ["bin/*.png"]},
    author="Roderick MacSween",
    author_email="macsweenroddy@gmail.com",
    license="MIT",
    long_description=open("README.txt").read(),
    scripts=[join("bin", "newproject.py"),
             join("bin", "exampleproject.py"),],
    classifiers=["Development Status :: 2 - Pre-Alpha",
                 "Intended Audience :: Developers",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: Implementation :: CPython",
                 "Topic :: Games/Entertainment",
                 "Topic :: Multimedia",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 "Topic :: Software Development :: Libraries :: pygame",
                 "License :: OSI Approved :: MIT License",],
)