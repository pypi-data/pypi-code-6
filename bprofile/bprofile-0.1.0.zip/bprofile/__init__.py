#####################################################################
#                                                                   #
# __init__.py                                                       #
#                                                                   #
# Copyright 2014, Chris Billington                                  #
#                                                                   #
# This file is part of the bprofile project (see                    #
# https://bitbucket.org/cbillington/bprofile) and is licensed under #
# the Simplified BSD License. See the LICENSE.txt file in the root  #
# of the project for the full license.                              #
#                                                                   #
#####################################################################

from .bprofile import BProfile
from __version__ import __version__

__doc__ = """
    This is the bprofile package version %s, a wrapper
    around profile/cProfile, gprof2dot and dot,
    providing a simple context manager for profiling
    sections of Python code and producing visual graphs
    of profiling results. See the documentation of
    bprofile.BProfile for more information and usage
    examples.
    """ %__version__

__all__ = ['BProfile']