# -*- coding: utf-8 -*-

# Copyright (c) 2008-2014 CoNWeT Lab., Universidad Politécnica de Madrid

# This file is part of Wirecloud.

# Wirecloud is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Wirecloud is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Wirecloud.  If not, see <http://www.gnu.org/licenses/>.


import codecs
import Cookie
from cStringIO import StringIO
import mimetypes
import os
import requests
import shutil
import stat
import sys
from tempfile import mkdtemp
from urllib2 import URLError, HTTPError
from urlparse import urlparse

from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.test import LiveServerTestCase
from django.test import TransactionTestCase
from django.test.client import Client
from django.utils import translation
from django.utils.importlib import import_module

from wirecloud.platform.localcatalogue.utils import install_resource
from wirecloud.platform.widget import utils as showcase
from wirecloud.proxy.views import WIRECLOUD_PROXY
from wirecloud.catalogue import utils as catalogue
from wirecloud.commons.utils import downloader
from wirecloud.commons.utils.remote import MobileWirecloudRemoteTestCase, WirecloudRemoteTestCase
from wirecloud.commons.utils.wgt import WgtDeployer, WgtFile


def cleartree(path):

    if os.path.islink(path):
        # symlinks to directories are forbidden, see bug #1669
        raise OSError("Cannot call cleartree on a symbolic link")

    names = []
    try:
        names = os.listdir(path)
    except os.error:
        pass

    for name in names:
        fullname = os.path.join(path, name)
        try:
            mode = os.lstat(fullname).st_mode
        except os.error:
            mode = 0
        if stat.S_ISDIR(mode):
            shutil.rmtree(fullname, ignore_errors=True)
        else:
            try:
                os.remove(fullname)
            except os.error:
                pass


def restoretree(backup_path, dest_path):
    cleartree(dest_path)

    names = []
    try:
        names = os.listdir(backup_path)
    except os.error:
        pass

    for name in names:
        srcname = os.path.join(backup_path, name)
        dstname = os.path.join(dest_path, name)

        try:
            mode = os.lstat(srcname).st_mode
        except os.error:
            mode = 0

        if stat.S_ISDIR(mode):
            shutil.copytree(srcname, dstname)
        else:
            shutil.copy2(srcname, dstname)


class DynamicWebServer(object):

    responses = {}

    def __init__(self, fallback=None):

        self.fallback = fallback

    def add_response(self, method, path, response_body):

        if path not in self.responses:
            self.responses[path] = {}

        self.responses[path][method] = response_body

    def clear(self):
        self.responses = {}

    def request(self, method, url, *args, **kwargs):

        parsed_url = urlparse(url)
        if parsed_url.path not in self.responses or method not in self.responses[parsed_url.path]:

            if self.fallback is not None:
                return self.fallback.request(method, url, *args, **kwargs)
            else:
                return {'status_code': 404, 'reason': 'Not Found'}

        response = self.responses[parsed_url.path][method]

        if callable(response):
            response = response(method, url, *args, **kwargs)

        return response


class LiveServer(object):

    def __init__(self):
        self._client = Client()

    def request(self, method, url, *args, **kwargs):

        parsed_url = urlparse(url)
        if parsed_url.path.startswith('/static/'):
            if method != 'GET':
                raise HTTPError('url', '405', 'Method not allowed', None, None)

            final_path = finders.find(parsed_url.path[8:])
            f = codecs.open(final_path, 'rb')
            contents = f.read()
            f.close()

            return {
                'headers': {
                    'Content-Type': mimetypes.guess_type(final_path, strict=False)[0],
                    'Content-Length': len(contents),
                },
                'content': contents,
            }
        else:
            return getattr(self._client, method.lower())(url)


class LocalFileSystemServer(object):

    def __init__(self, base_path):

        self.base_path = os.path.abspath(base_path)

    def request(self, method, url, *args, **kwargs):

        if method != 'GET':
            raise HTTPError('url', '405', 'Method not allowed', None, None)

        parsed_url = urlparse(url)
        final_path = os.path.normpath(os.path.join(self.base_path, parsed_url.path[1:]))
        if final_path.startswith(self.base_path) and os.path.isfile(final_path):
            f = codecs.open(final_path, 'rb')
            contents = f.read()
            f.close()

            return {
                'headers': {
                    'Content-Type': mimetypes.guess_type(final_path, strict=False)[0],
                    'Content-Length': len(contents),
                },
                'content': contents,
            }
        else:
            return {'status_code': 404, 'reason': 'Not Found'}


class StreamContent(object):

    def __init__(self, content):

        if not hasattr(content, '__iter__'):
            self._content = StringIO(content)
        else:
            self._content = content

    def read(self, *args, **kwargs):

        return self._content.read(*args, **kwargs)

    def stream(self, *args, **kwargs):

        return self._content.__iter__()


class FakeNetwork(object):

    old_download_function = None
    old_requests_request = None
    old_requests_get = None
    old_requests_post = None

    def __init__(self, servers={}):
        self._servers = servers

    def __call__(self, method, url, *args, **kwargs):
        parsed_url = urlparse(url)

        if 'data' not in kwargs or kwargs['data'] is None:
            kwargs['data'] = StringIO('')

        if parsed_url.scheme not in self._servers or parsed_url.netloc not in self._servers[parsed_url.scheme]:
            raise URLError('not valid')

        server = self._servers[parsed_url.scheme][parsed_url.netloc]
        return server.request(method, url, *args, **kwargs)

    def _prepare_response(self, res_info, url):

        res = requests.Response()
        res.url = res_info.get('url', url)
        res.status_code = res_info.get('status_code', 200)
        if 'reason' in res_info:
            res.reason = res_info['reason']

        if 'headers' in res_info:
            res.headers.update(res_info['headers'])

            if 'Set-Cookie' in res_info['headers']:
                cookies = Cookie.SimpleCookie()
                for entry in res_info['headers']['Set-Cookie'].split(','):
                    cookies.load(entry)
                res.cookies.update(cookies)

        res.raw = StreamContent(res_info.get('content', ''))

        return res

    def mock_requests(self):

        if self.old_requests_request is not None:
            return

        def request_mock(method, url, *args, **kwargs):
            res_info = self(method.upper(), url, *args, **kwargs)
            return self._prepare_response(res_info, url)

        def get_mock(url, *args, **kwargs):
            res_info = self('GET', url, *args, **kwargs)
            return self._prepare_response(res_info, url)

        def post_mock(url, *args, **kwargs):
            res_info = self('POST', url, *args, **kwargs)
            return self._prepare_response(res_info, url)

        self.old_requests_request = requests.request
        requests.request = request_mock
        self.old_requests_get = requests.get
        requests.get = get_mock
        self.old_requests_post = requests.post
        requests.post = post_mock

    def unmock_requests(self):
        requests.request = self.old_requests_request
        requests.get = self.old_requests_get
        requests.post = self.old_requests_post
        self.old_requests_request = None
        self.old_requests_get = None
        self.old_requests_post = None


class WirecloudTestCase(TransactionTestCase):

    @classmethod
    def setUpClass(cls):

        # Setup languages
        from django.conf import settings

        cls.old_LANGUAGES = settings.LANGUAGES
        cls.old_LANGUAGE_CODE = settings.LANGUAGE_CODE
        cls.old_DEFAULT_LANGUAGE = settings.DEFAULT_LANGUAGE
        settings.LANGUAGES = (('en', 'English'), ('es', 'Spanish'))
        settings.LANGUAGE_CODE = 'en'
        settings.DEFAULT_LANGUAGE = 'en'

        cls.shared_test_data_dir = os.path.join(os.path.dirname(__file__), '../test-data')

        # Mock network requests
        cls.network = FakeNetwork(getattr(cls, 'servers', {
            'http': {
                'localhost:8001': LocalFileSystemServer(os.path.join(os.path.dirname(__file__), '..', 'test-data', 'src')),
                'macs.example.com': LocalFileSystemServer(os.path.join(os.path.dirname(__file__), '..', 'test-data')),
                'example.com': DynamicWebServer(),
            },
        }))
        cls.network.mock_requests()

        # catalogue deployer
        cls.old_catalogue_deployer = catalogue.wgt_deployer
        cls.catalogue_tmp_dir_backup = mkdtemp()
        cls.catalogue_tmp_dir = mkdtemp()
        catalogue.wgt_deployer = WgtDeployer(cls.catalogue_tmp_dir)

        # showcase deployer
        cls.old_deployer = showcase.wgt_deployer
        cls.localcatalogue_tmp_dir_backup = mkdtemp()
        cls.tmp_dir = mkdtemp()
        showcase.wgt_deployer = WgtDeployer(cls.tmp_dir)

        restoretree(cls.tmp_dir, cls.localcatalogue_tmp_dir_backup)
        restoretree(cls.catalogue_tmp_dir, cls.catalogue_tmp_dir_backup)

        super(WirecloudTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):

        # deployers
        catalogue.wgt_deployer = cls.old_catalogue_deployer
        shutil.rmtree(cls.catalogue_tmp_dir_backup, ignore_errors=True)
        shutil.rmtree(cls.catalogue_tmp_dir, ignore_errors=True)
        showcase.wgt_deployer = cls.old_deployer
        shutil.rmtree(cls.localcatalogue_tmp_dir_backup, ignore_errors=True)
        shutil.rmtree(cls.tmp_dir, ignore_errors=True)

        # Restore previous language configuration
        from django.conf import settings

        settings.LANGUAGES = cls.old_LANGUAGES
        settings.LANGUAGE_CODE = cls.old_LANGUAGE_CODE
        settings.DEFAULT_LANGUAGE = cls.old_DEFAULT_LANGUAGE

        # Clear cache
        from django.core.cache import cache
        cache.clear()

        # Unmock network requests
        cls.network.unmock_requests()

        super(WirecloudTestCase, cls).tearDownClass()

    def setUp(self):

        # deployers
        restoretree(self.localcatalogue_tmp_dir_backup, self.tmp_dir)
        restoretree(self.catalogue_tmp_dir_backup, self.catalogue_tmp_dir)

        # clean example.com responses
        try:
            self.network._servers['http']['example.com'].clear()
        except:
            pass

        # cache
        from django.core.cache import cache
        cache.clear()

        # Restore English as the default language
        self.changeLanguage('en')

    def changeLanguage(self, new_language):

        from django.conf import settings

        settings.LANGUAGE_CODE = new_language
        settings.DEFAULT_LANGUAGE = new_language
        translation.activate(new_language)


def uses_extra_resources(resources, shared=False, public=True, users=(), groups=()):

    def wrap(test_func):

        def wrapper(self, *args, **kwargs):

            if shared:
                base = self.shared_test_data_dir
            else:
                base = self.test_data_dir

            for resource in resources:
                wgt_file = open(os.path.join(base, resource), 'rb')
                wgt = WgtFile(wgt_file)

                resource = install_resource(wgt, None, None, True)

                if public:
                    resource.public = True
                    resource.save()

                final_users = (User.objects.get(username=user) for user in users)
                resource.users.add(*final_users)

                final_groups = (Group.objects.get(name=group) for group in groups)
                resource.groups.add(*final_groups)

                wgt_file.close()

            return test_func(self, *args, **kwargs)

        wrapper.func_name = test_func.func_name
        return wrapper

    return wrap


class WirecloudSeleniumTestCase(LiveServerTestCase, WirecloudRemoteTestCase):

    fixtures = ('initial_data', 'selenium_test_data')
    __test__ = False

    @classmethod
    def setUpClass(cls):

        from django.conf import settings

        WirecloudRemoteTestCase.setUpClass.im_func(cls)

        cls.old_LANGUAGES = settings.LANGUAGES
        cls.old_LANGUAGE_CODE = settings.LANGUAGE_CODE
        cls.old_DEFAULT_LANGUAGE = settings.DEFAULT_LANGUAGE
        settings.LANGUAGES = (('en', 'English'),)
        settings.LANGUAGE_CODE = 'en'
        settings.DEFAULT_LANGUAGE = 'en'

        # Mock network requests
        cls.network = FakeNetwork(getattr(cls, 'servers', {
            'http': {
                'localhost:8001': LocalFileSystemServer(os.path.join(os.path.dirname(__file__), '..', 'test-data', 'src')),
                'macs.example.com': LocalFileSystemServer(os.path.join(os.path.dirname(__file__), '..', 'test-data')),
                'example.com': DynamicWebServer(),
            },
        }))
        cls.network.mock_requests()

        # catalogue deployer
        cls.old_catalogue_deployer = catalogue.wgt_deployer
        cls.catalogue_tmp_dir_backup = mkdtemp()
        cls.catalogue_tmp_dir = mkdtemp()
        catalogue.wgt_deployer = WgtDeployer(cls.catalogue_tmp_dir)

        # showcase deployer
        cls.old_deployer = showcase.wgt_deployer
        cls.localcatalogue_tmp_dir_backup = mkdtemp()
        cls.tmp_dir = mkdtemp()
        showcase.wgt_deployer = WgtDeployer(cls.tmp_dir)

        # deploy resource files
        operator_wgt_file = open(os.path.join(cls.shared_test_data_dir, 'Wirecloud_TestOperator_1.0.zip'), 'rb')
        operator_wgt = WgtFile(operator_wgt_file)
        catalogue.add_widget_from_wgt(operator_wgt_file, None, wgt_file=operator_wgt, deploy_only=True)
        showcase.wgt_deployer.deploy(operator_wgt)
        operator_wgt_file.close()

        widget_wgt_file = open(os.path.join(cls.shared_test_data_dir, 'Wirecloud_Test_1.0.wgt'))
        widget_wgt = WgtFile(widget_wgt_file)
        catalogue.add_widget_from_wgt(widget_wgt_file, None, wgt_file=widget_wgt, deploy_only=True)
        showcase.wgt_deployer.deploy(widget_wgt)
        widget_wgt_file.close()

        restoretree(cls.tmp_dir, cls.localcatalogue_tmp_dir_backup)
        restoretree(cls.catalogue_tmp_dir, cls.catalogue_tmp_dir_backup)

        LiveServerTestCase.setUpClass.im_func(cls)

        cls.network._servers['http'][cls.server_thread.host + ':' + str(cls.server_thread.port)] = LiveServer()

    @classmethod
    def tearDownClass(cls):

        from django.conf import settings

        WirecloudRemoteTestCase.tearDownClass.im_func(cls)

        # Unmock network requests
        cls.network.unmock_requests()

        # deployers
        catalogue.wgt_deployer = cls.old_catalogue_deployer
        shutil.rmtree(cls.catalogue_tmp_dir_backup, ignore_errors=True)
        shutil.rmtree(cls.catalogue_tmp_dir, ignore_errors=True)
        showcase.wgt_deployer = cls.old_deployer
        shutil.rmtree(cls.localcatalogue_tmp_dir_backup, ignore_errors=True)
        shutil.rmtree(cls.tmp_dir, ignore_errors=True)

        settings.LANGUAGES = cls.old_LANGUAGES
        settings.LANGUAGE_CODE = cls.old_LANGUAGE_CODE
        settings.DEFAULT_LANGUAGE = cls.old_DEFAULT_LANGUAGE

        super(WirecloudSeleniumTestCase, cls).tearDownClass()

    def setUp(self):

        from django.core.cache import cache

        restoretree(self.localcatalogue_tmp_dir_backup, self.tmp_dir)
        restoretree(self.catalogue_tmp_dir_backup, self.catalogue_tmp_dir)
        cache.clear()
        try:
            self.network._servers['http']['example.com'].clear()
        except:
            pass

        super(WirecloudSeleniumTestCase, self).setUp()


class MobileWirecloudSeleniumTestCase(LiveServerTestCase, MobileWirecloudRemoteTestCase):

    fixtures = ('initial_data', 'selenium_test_data')
    __test__ = False

    @classmethod
    def setUpClass(cls):

        from django.conf import settings

        MobileWirecloudRemoteTestCase.setUpClass.im_func(cls)

        cls.old_LANGUAGES = settings.LANGUAGES
        cls.old_LANGUAGE_CODE = settings.LANGUAGE_CODE
        cls.old_DEFAULT_LANGUAGE = settings.DEFAULT_LANGUAGE
        settings.LANGUAGES = (('en', 'English'),)
        settings.LANGUAGE_CODE = 'en'
        settings.DEFAULT_LANGUAGE = 'en'

        # Mock network requests
        cls.network = FakeNetwork(getattr(cls, 'servers', {
            'http': {
                'localhost:8001': LocalFileSystemServer(os.path.join(os.path.dirname(__file__), '..', 'test-data', 'src')),
                'macs.example.com': LocalFileSystemServer(os.path.join(os.path.dirname(__file__), '..', 'test-data')),
                'example.com': DynamicWebServer(),
            },
        }))
        cls.network.mock_requests()

        # catalogue deployer
        cls.old_catalogue_deployer = catalogue.wgt_deployer
        cls.catalogue_tmp_dir_backup = mkdtemp()
        cls.catalogue_tmp_dir = mkdtemp()
        catalogue.wgt_deployer = WgtDeployer(cls.catalogue_tmp_dir)

        # showcase deployer
        cls.old_deployer = showcase.wgt_deployer
        cls.localcatalogue_tmp_dir_backup = mkdtemp()
        cls.tmp_dir = mkdtemp()
        showcase.wgt_deployer = WgtDeployer(cls.tmp_dir)

        # deploy resource files
        operator_wgt_file = open(os.path.join(cls.shared_test_data_dir, 'Wirecloud_TestOperator_1.0.zip'), 'rb')
        operator_wgt = WgtFile(operator_wgt_file)
        catalogue.add_widget_from_wgt(operator_wgt_file, None, wgt_file=operator_wgt, deploy_only=True)
        showcase.wgt_deployer.deploy(operator_wgt)
        operator_wgt_file.close()

        widget_wgt_file = open(os.path.join(cls.shared_test_data_dir, 'Wirecloud_Test_1.0.wgt'))
        widget_wgt = WgtFile(widget_wgt_file)
        catalogue.add_widget_from_wgt(widget_wgt_file, None, wgt_file=widget_wgt, deploy_only=True)
        showcase.wgt_deployer.deploy(widget_wgt)
        widget_wgt_file.close()

        restoretree(cls.tmp_dir, cls.localcatalogue_tmp_dir_backup)
        restoretree(cls.catalogue_tmp_dir, cls.catalogue_tmp_dir_backup)

        LiveServerTestCase.setUpClass.im_func(cls)

        cls.network._servers['http'][cls.server_thread.host + ':' + str(cls.server_thread.port)] = LiveServer()

    @classmethod
    def tearDownClass(cls):

        from django.conf import settings

        MobileWirecloudRemoteTestCase.tearDownClass.im_func(cls)

        # Unmock network requests
        cls.network.unmock_requests()

        # deployers
        catalogue.wgt_deployer = cls.old_catalogue_deployer
        shutil.rmtree(cls.catalogue_tmp_dir_backup, ignore_errors=True)
        shutil.rmtree(cls.catalogue_tmp_dir, ignore_errors=True)
        showcase.wgt_deployer = cls.old_deployer
        shutil.rmtree(cls.localcatalogue_tmp_dir_backup, ignore_errors=True)
        shutil.rmtree(cls.tmp_dir, ignore_errors=True)

        settings.LANGUAGES = cls.old_LANGUAGES
        settings.LANGUAGE_CODE = cls.old_LANGUAGE_CODE
        settings.DEFAULT_LANGUAGE = cls.old_DEFAULT_LANGUAGE

        super(MobileWirecloudSeleniumTestCase, cls).tearDownClass()

    def setUp(self):

        from django.core.cache import cache

        restoretree(self.localcatalogue_tmp_dir_backup, self.tmp_dir)
        restoretree(self.catalogue_tmp_dir_backup, self.catalogue_tmp_dir)
        cache.clear()
        try:
            self.network._servers['http']['example.com'].clear()
        except:
            pass

        super(MobileWirecloudSeleniumTestCase, self).setUp()


DEFAULT_BROWSER_CONF = {
    'Firefox': {
        'CLASS': 'selenium.webdriver.Firefox',
    },
    'GoogleChrome': {
        'CLASS': 'selenium.webdriver.Chrome',
    },
}


def get_configured_browsers():

    from django.conf import settings

    return getattr(settings, 'WIRECLOUD_SELENIUM_BROWSER_COMMANDS', DEFAULT_BROWSER_CONF)

def wirecloud_selenium_test_case(classes, namespace=None, browsers=None):

    if browsers is None:
        browsers = get_configured_browsers()

    try:
        iter(classes)
    except TypeError:
        classes = (classes,)

    for class_name in classes:
        for browser_name in browsers:
            browser = browsers[browser_name]

            if isinstance(class_name, basestring):
                module_name, klass_name = class_name.rsplit('.', 1)
                tests_class_name = browser_name + klass_name
                module = import_module(module_name)
                klass_instance = getattr(module, klass_name)
            else:
                tests_class_name = browser_name + class_name.__name__
                klass_instance = class_name

            new_klass = type(
                tests_class_name,
                (klass_instance,),
                {
                    '__test__': True,
                    '_webdriver_class': browser['CLASS'],
                    '_webdriver_args': browser.get('ARGS', None),
                }
            )

            if namespace is not None:
                klass_namespace = namespace
            else:
                klass_namespace = sys.modules[klass_instance.__module__]

            try:
                setattr(klass_namespace, tests_class_name, new_klass)
            except AttributeError:
                klass_namespace[tests_class_name] = new_klass
wirecloud_selenium_test_case.__test__ = False
build_selenium_test_cases = wirecloud_selenium_test_case
