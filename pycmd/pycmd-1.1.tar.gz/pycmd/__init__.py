#
#

__version__ = "1.1"

from py.apipkg import initpkg

initpkg(__name__, dict(
    pylookup    = '.pylookup:main',
    pycountloc  = '.pycountloc:main',
    pycleanup   = '.pycleanup:main',
    pywhich     = '.pywhich:main',
    pysvnwcrevert = '.pysvnwcrevert:main',
    pyconvert_unittest = '.pyconvert_unittest:main',
))
