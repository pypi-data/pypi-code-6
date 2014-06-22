from distutils.core import setup
# Read in long description
long_description="""
You write stuff that looks like this, containing all of the information
you would ever need about a tool; options, test cases, metadata

.. code:: python

    from galaxygetopt.ggo import GalaxyGetOpt as GGO
    c = GGO(
        options=[
            ['int', 'An integer parameter', {'required': True, 'validate':
                                             'Int', 'default': 10}],
            ['float', 'A float', {'required': True, 'validate': 'Float',
                                  'default': 1e-4}],
            ['string', 'A string value', {'required': True, 'multiple': True,
                                          'default': ['Hello', 'World'],
                                          'validate': 'String'}],

And you get data back in a nice dict

.. code:: python

    {'int': 40, 'float': '1e-4', 'string': ['Hello', 'World'] }

Known Bugs
==========

Currently there is a known bug in the galaxy XML, under highly specific
circumstances. If you define a parameter that is

-  ``required``
-  ``hidden``
-  ``validate String`` (probably not a hard req)
-  ``_galaxy_specific``

and expect it to properly generate the value, it will not. See lines
206/207 of ``galaxygetopt/ggo.py`` for the current hack I use to get
around this.

Other
=====

This library features a number of subclasses of
``galaxygetopt.parameter.parameter``, all of which have myriad numbers
of options. In order to brutally test these, I have added a class
``galaxygetopt/tests/parameter_generator.py`` which can generate every
single possible combination of functional calls, given rules you
specify. You can then generate hundreds of objects with different sets
of options, which you can filter a subset out and test at will. See that
classes's documentation for more information.

"""

setup(name='galaxygetopt',
      version='0.9.2',
      description='Argparse Wrapper for Galaxy',
      author='Eric Rasche',
      author_email='rasche.eric@yandex.ru',
      url='https://cpt.tamu.edu/gitlab/cpt/pygetoptwrapper/',
      packages = ['galaxygetopt', 'galaxygetopt.parameter', 'galaxygetopt.writer'],
      license='GPL3',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Environment :: Console'
      ],
      long_description=long_description,
)
