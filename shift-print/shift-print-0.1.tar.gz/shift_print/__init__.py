# coding: utf-8

""" Module provides tools for shifting output from scopes wrapped with the 'with' statement.
    For example, this code:
        >>> import sys
        >>> from shift_print import shift_both, ShiftMore
        >>>
        >>> def test_print(depth, level=0):
        ...     ''' Test recursive printing
        ...     '''
        ...     if depth <= 0:
        ...         return
        ...     print "OUT:", level
        ...     print >>sys.stderr, "ERR:", level
        ...     print
        ...     print >>sys.stderr
        ...     with ShiftMore():
        ...         test_print(depth-1, level+1)
        ...
        >>> with shift_both(out_space=' +  ', err_space='  + ', level=1):
        ...     test_print(5)
        ... 

    Will produce this output:
         +  OUT: 0
          + ERR: 0
         +  
          + 
         +   +  OUT: 1
          +   + ERR: 1
         +   +  
          +   + 
         +   +   +  OUT: 2
          +   +   + ERR: 2
         +   +   +  
          +   +   + 
         +   +   +   +  OUT: 3
          +   +   +   + ERR: 3
         +   +   +   +  
          +   +   +   + 
         +   +   +   +   +  OUT: 4
          +   +   +   +   + ERR: 4
         +   +   +   +   +  
          +   +   +   +   + 
"""

from shift_print import (
    shift,
    shift_out,
    shift_err,
    shift_both,
    BasicShiftingStream,
    ShiftingStream,
    ShiftContext,
    ShiftPrintScope,
    ShiftStreamScope,
    ShiftMore,
    StdTrap,
    deep_print,
    deep_write
)