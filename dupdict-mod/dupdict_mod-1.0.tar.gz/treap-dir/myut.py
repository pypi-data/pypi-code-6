
#mport sys
import traceback
import exceptions

def require_exceptionless(description, fn):
    try:
        fn()
    except:
        print 'failed: %s' % description
        print description
        traceback.print_exc()
        print '======'
    else:
#        print 'passed: %s' % description
#        print '======'
        pass

def require_exceptions(fn, excs):
    try:
        fn()
    except tuple(excs):
        pass
    except:
        traceback.print_exc()
        print '======'
    else:
        raise exceptions.AssertionError

def assertEqual(x, y):
    #print 'x, y:', x, y
    if x != y:
        print '%s != %s' % (str(x), str(y))
        raise exceptions.AssertionError
        
def assertTrue(boolean):
    if not boolean:
        raise exceptions.AssertionError

