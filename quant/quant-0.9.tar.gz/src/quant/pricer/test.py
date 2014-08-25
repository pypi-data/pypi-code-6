import unittest
import quant.pricer.blackscholestest
import quant.pricer.binomialtreetest
import quant.pricer.montecarlotest
import quant.pricer.blackscholeslocalvoltest
def suite():
    suites = [
        quant.pricer.blackscholestest.suite(),
        quant.pricer.binomialtreetest.suite(),
        quant.pricer.montecarlotest.suite(),
        quant.pricer.blackscholeslocalvoltest.suite(),
    ]
    return unittest.TestSuite(suites)

# Todo: More business rules.
# Todo: Put-call parity.

