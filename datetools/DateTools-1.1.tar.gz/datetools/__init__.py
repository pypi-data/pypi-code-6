"""
Date tools
----------

Collection of useful extensions to Python's datetime
module in the standard library. These functions occur
so frequently while scripting and have been rewritten
in so many places that it makes sense to have a
site-packages variant available at;

``export PYTHONPATH=~frrn/ofrd/lib/python2.7/site-packages:${PYTHONPATH}``

"""
# Functions
from core import (convert,
                  daterange,
                  gaps,
                  shiftdate,
                  shiftdates,
                  strptimes,
                  datewindow)
# Constants
from core import (DAY,
                  HOUR,
                  MIN)
