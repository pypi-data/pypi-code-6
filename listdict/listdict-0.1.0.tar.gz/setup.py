from distutils.core import setup
setup(
    name='listdict',
    version='0.1.0',
    description='This is a container class that acts like a list and a dictionary and a structure.',
    long_description="The \"append\" method adds items to the list. If there's a second parameter, it is a label that can subsequently be used as an index, but that also is stored in the main dictionary. This means that an element could be read or written as, for example, ld[1], ld[\"somelabel\"], and ld.somelabel.",
    license='LICENSE.txt',
    py_modules=['listdict'],
    provides=['listdict', ],
    author="Larry Fenske",
    author_email="pypi@towanda.com",
    url="https://github.com/LFenske/ListDict",
)
