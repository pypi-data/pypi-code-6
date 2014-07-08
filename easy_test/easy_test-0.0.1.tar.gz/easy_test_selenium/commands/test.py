from importlib import import_module
from easy_test_selenium.test_case_principal import TestCasePrincipal
from easy_test_selenium.configuration import Settings
from easy_test_selenium import utils
from types import MethodType

def run_command(name='all'):
    test = TestCasePrincipal()
    settings = Settings()
    conf = settings.getConfiguration()
    utils.TEST = name

    for driver in conf.WEB_DRIVERS:
        utils.DRIVER_INSTANCE = driver
        test.runTest()
    print 'Test Finished'