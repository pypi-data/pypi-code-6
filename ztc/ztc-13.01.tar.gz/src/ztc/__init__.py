#!/usr/bin/env python

import sys

def notsupported(err=None):
    """
    DEPRECATED, will be removed!
    
    Executed when item is not supported
    Params:
     * err: Exception - reason exception object
    """
    msg = "NOT_SUPPORTED"
    if err: msg += ": " + str(err)
    print(msg)
    if isinstance(err, Exception): raise err
    sys.exit(1)