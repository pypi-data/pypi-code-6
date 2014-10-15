import unittest,sys,threading
import flasksupport
import httpretty

class TestCase(unittest.TestCase):
                
    def test_abortSystem(self):
        """somethign is not letting python die - likely has to do with httpretty
        """
        for x in threading.enumerate():
            print(x)
        delattr(httpretty.core.FakeSockFile,'close')
        for x in flasksupport.httpretty_fix:
            print(x)
            x.close()
        httpretty.disable()
        httpretty.reset()
        