from unittest import TestCase
from apy.main import Application
from apy.http import Request
from os import getenv


class ApplicationTestCase(TestCase):
    def __init__(self, methodName='runTest'):
        TestCase.__init__(self, methodName)
        self._application = False

    def boot(self, application_environment='test', environment_variable_of_config_dir='APPLICATION_CONFIG_DIR'):
        application_config_dir = getenv(environment_variable_of_config_dir, None)
        if application_config_dir is None:
            raise ApplicationTestCaseException('Application not configured yet.')
        self._application = Application(application_environment, application_config_dir)

    def request(self, method, path=None, query=None, data=None, files=None, headers=None, host='', protocol='http', remote_ip=None, version=None):
        if not self._application:
            raise ApplicationTestCaseException('Application not booted yet')
        request = Request(
            method,
            path,
            query,
            data,
            files,
            headers,
            host,
            protocol,
            remote_ip,
            version
        )
        response = self._application.do_request(request)
        return response


class ApplicationTestCaseException(Exception):
    pass
