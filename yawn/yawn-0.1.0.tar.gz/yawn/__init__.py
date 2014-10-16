# -*- coding: utf-8 -*-

import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_driver(browser, seleniumip):
    if seleniumip:
        if browser.lower() == 'chrome':
            # Chrome headless
            d = DesiredCapabilities.CHROME
            d['loggingPrefs'] = { 'browser':'ALL', 'performance': 'INFO' }
            return webdriver.Remote(
                command_executor='http://{}:4444/wd/hub'.format(
                    seleniumip,
                ),
                desired_capabilities=d,
            )
        elif browser.lower() == 'ie8':
            # IE8 in VM
            d = DesiredCapabilities.INTERNETEXPLORER
            return webdriver.Remote(
                command_executor='http://{}:4444/wd/hub'.format(
                    seleniumip,
                ),
                desired_capabilities=d,
            )
        elif browser.lower() == 'firefox':
            print "Firefox"
            d = DesiredCapabilities.FIREFOX
            d['loggingPrefs'] = {'browser': 'ALL', 'client': 'ALL', 'driver': 'ALL', 'performance': 'ALL', 'server': 'ALL'}
            return webdriver.Remote(
                command_executor='http://{}:4444/wd/hub'.format(
                    seleniumip,
                ),
                desired_capabilities=d,
            )
        else:
            raise ValueError(
                'Unsupported browser {} for remote selenium'.format(browser)
            )
    else:
        if browser.lower() == 'chrome':
            return webdriver.Chrome()
        elif browser.lower() == 'firefox':
            d = DesiredCapabilities.FIREFOX
            d['loggingPrefs'] = {'browser': 'ALL', 'client': 'ALL', 'driver': 'ALL', 'performance': 'ALL', 'server': 'ALL'}
            fp = webdriver.FirefoxProfile()
            # fp.set_preference('webdriver.log.file', 'webdriver.log')
            fp.add_extension(extension='browser/firefox/firebug-2.0.4-fx.xpi')
            fp.add_extension(extension='browser/firefox/consoleExport-0.5b6.xpi')
            fp.set_preference('javascript.options.showInConsole', 'true')
            fp.set_preference('browser.dom.window.dump.enabled', 'true')
            fp.set_preference('extensions.firebug.consoleexport.active', 'true')
            fp.set_preference('extensions.firebug.consoleexport.serverURL', 'http://localhost:8888')
            fp.set_preference("extensions.firebug.currentVersion", "2.0.4")
            fp.set_preference("extensions.firebug.console.enableSites", 'true')
            fp.set_preference("extensions.firebug.net.enableSites", 'true')
            fp.set_preference("extensions.firebug.script.enableSites", 'true')
            fp.set_preference("extensions.firebug.allPagesActivation", 'on')
            fp.set_preference("extensions.firebug.defaultPanelName", 'console')
            fp.set_preference("extensions.firebug.consoleexport.active", 'true')
            # This seems to have to be an absolute path
            fp.set_preference(
                "extensions.firebug.consoleexport.logFilePath",
                os.path.join(os.getcwd(), 'browser', 'firefox', 'console.log')
            )
            return webdriver.Firefox(capabilities=d, firefox_profile=fp)
        elif browser.lower() == 'safari':
            if not os.environ.get('SELENIUM_SERVER_JAR'):
                os.environ['SELENIUM_SERVER_JAR'] = os.path.join('browser', 'safari', 'selenium-server-standalone-2.43.1.jar')
            # return webdriver.Safari(capabilities=DesiredCapabilities.SAFARI)
            return webdriver.Safari()
        raise ValueError('Unknown combination: browser {!r} {!r}'.format(browser, seleniumip))

