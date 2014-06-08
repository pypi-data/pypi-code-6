import time
import sys

def init(msg):
    '''
        init_letter(msg) -> str
        Prints a message in an interative way
    '''
    
    print "%s" % msg,
    time.sleep(1)
    print ".",
    time.sleep(1)
    print ".",
    time.sleep(1)
    print "."
    time.sleep(1)

def show(msg):
    '''
        show(msg) -> str
        Prints a message in an interative way
    '''
    print >> sys.stderr, "** %s **" % msg
