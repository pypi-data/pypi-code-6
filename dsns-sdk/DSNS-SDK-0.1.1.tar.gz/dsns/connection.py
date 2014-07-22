import json
import urllib

from requests import Request, Session
from requests.adapters import HTTPAdapter

from django.conf import settings

from dsns.app_settings import HTTP_SSL
from dsns import AUTH_TOKEN, HOST


class Config(dict):
    """
    a dottable dict in which attributes
    can be accessed using dot notation
    Ex:
    >>a = {"name": "hari"}
    >>a.name
    >>a.age=34
    """
    def __init__(self, **kwargs):
        super(Config, self).__init__(**kwargs)
        self.__dict__ = self


class ResponseFormator(object):
    """
    Response formator class which parse response
    based on format defined in config
    """
    def __init__(self, resp_format, response):
        self.response = response
        self.resp_format = resp_format

    def dict2xml(self, d, root="xml"):
        op = lambda tag: '<' + tag + '>'
        cl = lambda tag: '</' + tag + '>'
        ml = lambda v, xml: xml + op(key) + str(v) + cl(key)
        xml = op(root) if root else ""
        for key, vl in d.iteritems():
            vtype = type(vl)
            if vtype is list:
                for v in vl:
                    xml = ml(v, xml)
            if vtype is dict:
                xml = ml(self.dict2xml(vl, None), xml)
            if vtype is not list and vtype is not dict:
                xml = ml(vl, xml)
        xml += cl(root) if root else ""
        return xml

    def response_dict(self):
        try:
            r = json.loads(self.response.content)
            return r
        except ValueError, e:
            return None

    def response_json(self):
        return self.response.content

    def response_xml(self):
        d = self.response_dict()
        return self.dict2xml(d)

    def get_status_code(self):
        return self.response.status_code


class BaseConnection(object):
    """
    Base connection class to create connection
    with dsns application server
    """
    __formator_class = ResponseFormator
    config = Config(
        domain=HOST, https=False, resp_format='json')

    def __init__(self, method="GET",
                 proxy_host=None, timeout=20,
                 proxy_port=80, **kwargs):

        self.response = None
        self.request = None
        self.method = method
        self.timeout = timeout
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.headers = dict()
        self.proxies = dict()
        self.query_params = dict()
        self.secret_key = AUTH_TOKEN
        if self.proxy_host:
            proxy = 'http://%s:%s' % (self.proxy_host, self.proxy_port)
            self.proxies = {'http': proxy, 'https': proxy}
        self.session = Session()
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))

    def _reset(self):
        self.request = None
        self.response = None

    def build_request_headers(self):
        self.headers.update(**{
            "content-type": "application/x-www-form-urlencoded",
            "accept": "application/json",
            "Authorization": "Token %s" % AUTH_TOKEN})

    def build_request(self, data=None):
        self.build_request_headers()
        url = "%s://%s%s" % (
            HTTP_SSL[self.config.https],
            self.config.domain,
            self.config.uri)
        if self.query_params:
            url = "%s?%s" % (
                url, urllib.urlencode(self.query_params))
        request = Request(
            self.method, url, data=data,
            headers=self.headers)
        self.request = request.prepare()

    def execute_request(self):
        self.response = self.session.send(
            self.request, verify=False, proxies=self.proxies,
            timeout=self.timeout, allow_redirects=True)

    def execute(self, data=None):
        self._reset()
        self.build_request(data)
        self.execute_request()
        f = BaseConnection.__formator_class(
            self.config.resp_format, self.response)
        return f
