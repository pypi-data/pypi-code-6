import os
from setuptools import setup, find_packages


long_description = """
subdicts
========

A small python utility which parses nested-keys in dictionaries into sub-dictionaries.

####Installation

This package can be installed from PyPI using `pip`. Make sure you have `pip` installed 
then run:

```
$ pip install subdicts
```

#####Installation Using Buildout

If you're using __Buildout__ and want to use __subdicts__ you can do so by adding the 
following lines to your `buildout.cfg` file:

```
[subdicts]
recipe = zc.recipe.egg:eggs
eggs = subdicts == <subdicts_version_number>
```

and appending `subdicts` to your `buildout:parts`.

####Usage

This package has one method, `subdicts.utils.parse`, which does the parsing.

```
from subdicts.utils import parse

dict = {'person[firstname]': 'arnelle', 'person[lastname]': 'balane'}
parsed = parse(dict)

# parsed = {'person': {'firstname': 'arnelle', 'lastname': 'balane'}}
```

####Contributing

To contribute to this mini-project just fork this repository, clone your forked repository 
and run buildout inside the project directory.

```
$ git clone git@github.com:arnellebalane/subdicts.git
$ cd subdicts
$ ./bin/buildout
```

This will take care of retrieving the project's dependencies.

When contributing new code to the project, please test your code. The test files are 
located inside the `src/subdicts/tests` directory. To run the tests simply do:

```
$ ./bin/test
```

Merging your code into this main repository must be done through pull requests.

####Bugs and Issues

If you find any bugs and issues in this project, please report them by opening an
issue here.

####Todo

- properly parse compicated dictionary keys, especially those containing inner `[` and 
  `]` characters (e.g. `person[name[]]`)
"""


setup(
    name = 'subdicts',
    version = '1.0.2',
    url = 'https://github.com/arnellebalane/subdicts',
    license = 'MIT',
    description = 'A small python utility which parses nested-keys in dictionaries into sub-dictionaries.',
    long_description = long_description,
    author = 'Arnelle Balane',
    author_email = 'arnellebalane@gmail.com',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
    test_suite = 'subdicts',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ]
)
