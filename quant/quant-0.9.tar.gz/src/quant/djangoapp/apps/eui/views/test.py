import unittest

def suite():
    import quant.djangoapp.apps.eui.views.welcometest
    import quant.djangoapp.apps.eui.views.apitest
    suites = [
        quant.djangoapp.apps.eui.views.welcometest.suite(),
        quant.djangoapp.apps.eui.views.apitest.suite(),
    ]
    return unittest.TestSuite(suites)

