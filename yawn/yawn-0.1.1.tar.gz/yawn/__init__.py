# -*- coding: utf-8 -*-

import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_driver(
    browser,
    seleniumip,
    firefox_files_dir=None,
):
    if firefox_files_dir is None:
        firefox_files_dir = os.environ.get('FIREFOX_FILES_DIR')
    if seleniumip:
        if browser.lower() == 'chrome':
            # Chrome headless
            d = DesiredCapabilities.CHROME
            d['loggingPrefs'] = {
                'browser': 'ALL',
                'performance': 'INFO',
            }
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
            # Firefox
            d = DesiredCapabilities.FIREFOX
            d['loggingPrefs'] = {
                'browser': 'ALL',
                'client': 'ALL',
                'driver': 'ALL',
                'performance': 'ALL',
                'server': 'ALL',
            }
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
            d['loggingPrefs'] = {
                'browser': 'ALL',
                'client': 'ALL',
                'driver': 'ALL',
                'performance': 'ALL',
                'server': 'ALL',
            }
            fp = webdriver.FirefoxProfile()
            if firefox_files_dir is not None:
                fp.add_extension(
                    extension='{}/firebug-2.0.4-fx.xpi'.format(
                        firefox_files_dir,
                    ),
                )
                fp.add_extension(
                    extension='{}/consoleExport-0.5b6.xpi'.format(
                        firefox_files_dir,
                    ),
                )
                for preference, value in [
                    # ('webdriver.log.file', 'webdriver.log'),
                    ('javascript.options.showInConsole', 'true'),
                    ('browser.dom.window.dump.enabled', 'true'),
                    ('extensions.firebug.consoleexport.active', 'true'),
                    ('extensions.firebug.currentVersion', '2.0.4'),
                    ('extensions.firebug.console.enableSites', 'true'),
                    ('extensions.firebug.net.enableSites', 'true'),
                    ('extensions.firebug.script.enableSites', 'true'),
                    ('extensions.firebug.allPagesActivation', 'on'),
                    ('extensions.firebug.defaultPanelName', 'console'),
                    ('extensions.firebug.consoleexport.active', 'true'),
                    (
                        'extensions.firebug.consoleexport.serverURL',
                        'http://localhost:8888',
                    ),
                    (
                        'extensions.firebug.consoleexport.logFilePath',
                        # This seems to have to be an absolute path
                        os.path.join(
                            os.abspath(firefox_files_dir),
                            'console.log'
                        ),
                    ),
                ]:
                    fp.set_preference(preference, value)
            return webdriver.Firefox(capabilities=d, firefox_profile=fp)
        elif browser.lower() == 'safari':
            if not os.environ.get('SELENIUM_SERVER_JAR'):
                raise KeyError(
                    'No SELENIUM_SERVER_JAR variable has been set. This '
                    'should point to a recent version of the '
                    'selenium-server-standalone-2.xxx.jar file.'
                )
            return webdriver.Safari()
        raise ValueError(
            'Unknown combination: browser {!r} {!r}'.format(
                browser,
                seleniumip,
            )
        )
