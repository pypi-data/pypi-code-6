#! /usr/bin/python
 
import setuptools
 
setuptools.setup(
    name = "EinSumConv",
    description = "The EinSumConv package builds on sympy and supports calculations according to Einstein summation convention.",
    keywords = "einstein summa sympy index tensor",
    install_requires = ["sympy>=0.7.5"],
    version = "0.0.2",
    author = "Linda Linsefors",
    author_email = "linda.linsefors@gmail.com",
    license = "BSD",
    url = "https://github.com/LindaLinsefors/EinSumConv",
    packages=['EinSumConv'],
)
