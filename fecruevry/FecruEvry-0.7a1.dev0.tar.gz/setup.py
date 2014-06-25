from setuptools import setup
import os.path
__dir__ = os.path.dirname(os.path.abspath(__file__))

setup(
    name='FecruEvry',
    license='BSD',
    py_modules=['fecru'],
    version='0.7a1.dev0',
    install_requires=['requests'],

    description='A python client to the Atlassian FECRU REST API',
    long_description=open(os.path.join(__dir__, 'README.rst')).read(),

    author='Christopher Richard Dobbs',
    author_email='christopher.dobbs@evry.com',
    url='https://github.com/dobbscr/python-fecru',

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration :: Authentication/Directory",
    ]
)
