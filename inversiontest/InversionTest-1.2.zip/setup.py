from setuptools import setup

setup(
    name='InversionTest',
    version='1.2',
    description='Sequence Permutation Similarity and Hypothesis Testing Package',
    author='Benjamin D. Nye',
    author_email='benjamid@seas.upenn.edu',
    url='https://sites.google.com/site/benjaminnye/',
    packages=['InversionTest','InversionTest.Tests'],
    include_package_data = True,
    #package_data={'docs': ['Documentation/*.*'],
    #              'examples':['Examples/*.*']},
      long_description="""\
          Library for inversion counting which can adjust for ties and censored data
         (e.g. left censored, right censored, etc). The intention of this library is
         to examine the distance from the sequence of elements to some reference sequence.
         It is also calculates an exact PMF of the distribution for inversion counts under
         the case where all permutations are equally likely, as well as a normal approximation
         for this same distribution.  Wilcoxan and sign tests are provided for hypothesis testing,
         where a group of permutations are compared against a single reference sequence.  This
         sort of testing would be needed for situations where a distribution of collected
         sequences might be compared against a "known correct" reference sequence.
      """,
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python",
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Science/Research",
          "Topic :: Scientific/Engineering :: Mathematics",
      ],
      keywords='inversion counts statistics software hypothesis testing censored ties',
      license='APL 2.0',
      install_requires=[],
      )
