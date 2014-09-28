
from setuptools import setup, find_packages

setup(
    name="bbking",
    version="0.0.1",
    description="A Django BBCode Parser",
    author="Rev. Johnny Healey",
    author_email="rev.null@gmail.com",
    license="GPL3",
    install_requires = [
        "ply==3.4",
        "django==1.4.10",
        "south==0.7.3"
      ],
    packages=find_packages(),
    package_data={
        'bbking':['templates/bbking/tags/*.html'],
    })
