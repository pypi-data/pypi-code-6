from simplelog import SL, log
from simplelog.decorators import *
import logging
from settings import SIMPLELOG
from filters import NullFilter
import sys

#class ContextM(object):
    #def __init__(self):
        #pass

    #def __enter__(self):
        #print("entering context")
        #return {}

    #def __exit__(self, exc_type, exc_val, exc_tb):
        #print("exiting context")
        #import pdb; pdb.set_trace()

#print("start")

#with ContextM() as fh:
    #print("in context")
#print("stop")
#sys.exit(0)


###
log("program has started")

@log_exception
@quiet()
def func():
    """
    Fun docs
    """
    print("hello from func")
    log("func has finished executing")
    raise ValueError

logger = SL

#func()
#log("program has finished")
