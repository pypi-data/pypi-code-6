import os
from setuptools import setup


setup(name='maproxy',

    version = "0.0.4",
    author = "Zvika Ferentz",
    author_email = "zvika.ferentz@gmail.com",
    description = ("My first attempt to create a simple and awesome "
                   "TCP proxy using Tornado"),
    #long_description=open('README').read(),


    py_modules=['src/maproxy'],
      )
