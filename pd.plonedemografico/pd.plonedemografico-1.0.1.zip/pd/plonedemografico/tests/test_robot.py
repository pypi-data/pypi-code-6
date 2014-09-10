from  pd.plonedemografico.testing import PD_PLONEDEMOGRAFICO_FUNCTIONAL_TESTING
from plone.testing import layered
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("robot_test.txt"),
                layer=PD_PLONEDEMOGRAFICO_FUNCTIONAL_TESTING)
    ])
    return suite