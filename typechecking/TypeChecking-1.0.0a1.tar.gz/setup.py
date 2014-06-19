from setuptools import setup

setup(
    name='TypeChecking',
    version='1.0.0a1',
    py_modules=['typechecking'],

    author='Kevin Norris',
    author_email='nykevin.norris@gmail.com',
    description='Run-time type checking for Python 3.4',
    long_description=
"""An informal standard for function annotations, and a type checker for it.

TypeChecking is a standard way of writing function annotations that's probably
pretty similar to whatever you're already doing.  See the home page for
specifics.  This package provides a run-time type checker for that standard.

""",
    license='BSD',
    keywords='type checking annotation',
    classifiers=[
                 'Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python :: 3.4',
                 'Topic :: Software Development :: Libraries :: Python '
                 'Modules',
                 'Topic :: Software Development :: Testing',
                ],
    url='http://bitbucket.com/NYKevin/typechecking',
)
