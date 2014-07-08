from importlib import import_module
from easy_test_selenium import utils
from easy_test_selenium.configuration import Settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import sys


class TestCasePrincipal(unittest.TestCase):
    def setUp(self):
        print 'ejecuto el set up'
        self.setting = Settings()
        self.conf = self.setting.getConfiguration()
        self.driver = self.get_driver(utils.DRIVER_INSTANCE)
        self.driver.implicitly_wait(self.conf.IMPLICITLY_WAIT)
        self.base_url = self.conf.URL_BASE
        self.verificationErrors = []
        self.accept_next_alert = True
        self.debug = self.conf.DEBUG

    def test_main(self):
        if utils.TEST == 'all':
            for app in self.conf.TEST_APPS:
                test_case = import_module('%s.test_case'%app)
                test_case.main(self)
        else:
            if utils.TEST in self.conf.TEST_APPS:
                test_case = import_module('%s.test_case'%utils.TEST)
                test_case.main(self)
            else:
                raise Exception("There is no test case called %s in this project"%name)
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def get_driver(self, driver):
        browser = driver['browser']
        path = 'path' in driver and driver['path'] or None
        my_driver =  None
        if browser=='chrome':
            my_driver = path is not None and webdriver.Chrome(path) or webdriver.Chrome()
        elif browser=='ie':
            my_driver = path is not None and webdriver.Ie(path) or webdriver.Ie()
        elif browser=='firefox':
            if path is not None:
                binary = FirefoxBinary(path)
                my_driver = webdriver.Firefox(firefox_binary=binary)
            else:
                my_driver = webdriver.Firefox()
        elif browser=='phantom':
            my_driver = path is not None and webdriver.PhantomJS(path) or webdriver.PhantomJS()
        elif browser=='opera':
            my_driver = path is not None and webdriver.Opera(path) or webdriver.Opera()
        elif browser=='safari':
            my_driver = path is not None and webdriver.Safari(path) or webdriver.Safari()
        return my_driver

    def runTest(self):
        if __name__ == 'easy_test_selenium.test_case_principal':
            unittest.main(module='test_case_principal', argv=sys.argv[:1], exit=False)

if __name__ == "__main__":
    unittest.main()