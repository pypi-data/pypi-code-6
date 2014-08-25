import unittest

def suite():
    import quant.markettest
    import quant.domtest
    import quantdsl.test
    import quant.priceprocess.test
    import quant.contracttype.test
    import quant.pricer.test
    import quant.leastsquarestest
    import quant.djangoapp.apps.eui.views.test
    suites = [
        quant.markettest.suite(),
        quant.domtest.suite(),
        quantdsl.test.suite(),
        quant.priceprocess.test.suite(),
        quant.contracttype.test.suite(),
        quant.pricer.test.suite(),
        quant.leastsquarestest.suite(),
        #quant.djangoapp.apps.eui.views.test.suite(),
    ]
    return unittest.TestSuite(suites)

