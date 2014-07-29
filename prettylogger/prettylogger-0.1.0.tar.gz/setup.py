from setuptools import setup, find_packages


long_description = """
prettylogger
============

Logs things (dicts, tuples, lists, etc) in color and beautiful format.

####Installation

This package can be installed from PyPI using `pip`. Make sure you have `pip` 
installed then run:

```
$ pip install prettylogger
```

#####Installation Using Buildout

If you're using Buildout and want to use prettylogger you can do so by adding 
the following lines to your `buildout.cfg` file:

```
[prettylogger]
recipe = zc.recipe.egg
eggs = prettylogger
```

and appending `prettylogger` to your `buildout:parts`.

####Usage

Logging beautifully formatted things is as easy as:

```
from prettylogger.utils import log

thing = {'name': 'prettylogger', 'version': '0.1.0'}
mode = 'rb' # Discussion below
log(thing, mode)
```

And it will log the following: 

![prettylogger output](http://i.imgur.com/HnbrCtj.png "prettylogger output")

#####Formatting Options

The `mode` parameter for the `log` function is a string with each character 
being one of the following:

- `p`: print the thing in purple
- `c`: print the thing in cyan
- `y`: print the thing in yellow
- `g`: print the thing in green
- `r`: print the thing in red
- `b`: print the thing in bold characters

So the `mode` used in the example above, `rb`, tells the `log` method to print
the thing in color red and bold characters.

####Contributing

To contribute to this mini-project just fork this repository, clone your forked 
repository and run buildout inside the project directory.

```
$ git clone git@github.com:arnellebalane/prettylogger.git
$ cd prettylogger
$ ./bin/buildout
```

This will take care of retrieving the project's dependencies.

When contributing new code to the project, please test your code. The test specs
are in the `src/prettylogger/tests.py` file. To run the tests simply do:

```
$ ./bin/test
```

Merging your code into this main repository must be done through pull requests.

####Bugs and Issues

If you find any bugs and issues in this project, please report them by opening 
an issue here.
"""


setup(
    name='prettylogger',
    version='0.1.0',
    url='http://github.com/arnellebalane/prettylogger',
    license='MIT',
    description='Logs things in color and beautiful format.',
    long_description=long_description,
    author='Arnelle Balane',
    author_email='arnellebalane@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['setuptools'],
    test_suite='prettylogger'
)