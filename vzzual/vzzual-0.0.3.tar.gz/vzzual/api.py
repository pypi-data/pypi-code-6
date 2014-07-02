
import os.path
import logging
import json
import time
import requests

base_url = "https://api.vzzual.com/"
api_key = None
logger = logging.getLogger('vzzual')
logging_enabled = True


def init(token, **kwargs):
    global api_key, logger, logging_enabled
    api_key = token
    log = kwargs.pop('log', True)
    if not log:
        logging_enabled = False
        logger.setLevel(logging.CRITICAL)  # effectively disables the logger
    else:
        logger.setLevel(kwargs.pop('log_level', logging.DEBUG))


def log(level, *args, **kwargs):
    if logging_enabled:
        method = getattr(logger, level)
        method(*args, **kwargs)


def token_auth():
    if not api_key:
        raise RuntimeError("API key not set. Use vzzual.init(key).")
    auth = {"Authorization": "Token " + api_key,
            "Content-Type": "application/json"}
    return auth


def _api_request(method, url, data=None):
    headers = token_auth()
    if data:
        data = json.dumps(data)
    log('debug', "{}: {}\n parameter: {}".format(method, url, data))
    r = getattr(requests, method)(url, data=data, headers=headers)
    if not r.ok:
        try:
            detail = ": {}".format(r.json()['detail'])
        except (KeyError, ValueError) as e:
            detail = e
        raise RuntimeError("Error {} occured {}".format(
                           r.status_code, detail))
    if r.text:
        return r.json()
    else:
        return None


def get_filters():
    return _api_request("get", base_url + "filters/")['results']


class APIResource(object):
    resource_type = None

    def __init__(self, json=None):
        if json is None:
            json = {}
        self._json_data = json
        for key in json:
            setattr(self, key, json[key])

    @classmethod
    def create(cls, **kwargs):
        r = _api_request("post", base_url + cls.resource_type + "/", kwargs)
        return cls(r)

    @classmethod
    def find(cls, url):
        r = _api_request("get", url)
        return cls(r)

    @classmethod
    def all(cls):
        r = _api_request("get", cls.resource_url())
        return [item['url'] for item in r['results']]

    def delete(self):
        _api_request("delete", self.url)

    @classmethod
    def resource_url(cls):
        return base_url + cls.resource_type + "/"

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               json.dumps(self._json_data))

    def __str__(self):
        return self.__repr__()


class Request(APIResource):
    resource_type = "requests"

    def submit(self):
        _api_request("put", self.submit_url)

    def get_results(self, wait=True, wait_timeout=1):
        r = _api_request("get", self.results_url)
        if wait:
            while True:
                log('debug', 'Waiting for results ...')
                time.sleep(wait_timeout)
                r = _api_request("get", self.url)
                if r['state'] in ("done", "error"):
                    log('debug', 'Got results:')
                    return self.get_results(wait=False)
        else:
            self.update_json_data()
            return r['results']

    def get_files(self):
        r = _api_request("get", self.files_url)
        return [File(res) for res in r['results']]

    def get_logs(self):
        r = _api_request("get", self.logs_url)
        return r['results']

    def get_errors(self):
        r = _api_request("get", self.errors_url)
        return r['results']

    def add_files(self, paths, visibility='private'):
        uploaded_files = []
        if not isinstance(paths, (tuple, list)):
            paths = [paths]
        for path in paths:
            if path.startswith('http://') or path.startswith('https://'):
                out = _api_request(
                    'post', self.files_url,
                    data={'url': path, 'visibility': visibility})
            else:
                out = self._upload_file(path, visibility)
            if out:
                uploaded_files.append(File(out))

        return uploaded_files

    def _upload_file(self, file_path, visibility='private'):
        headers = token_auth()
        headers.pop('Content-Type')
        with open(file_path, 'rb') as fp:
            fn = os.path.basename(file_path)
            req = requests.post(self.files_url,
                                files={'file': (fn, fp)},
                                data={'visibility': visibility},
                                headers=headers)
        if not req.ok:
            raise RuntimeError(req.content)
        return req.json()

    def update_json_data(self):
        data = self.__class__.find(self.url)._json_data
        for key in data:
            setattr(self, key, data[key])


class File(APIResource):
    resource_type = "files"

    @classmethod
    def create(cls, **kwargs):
        if 'image' in kwargs:
            file_name = kwargs.pop('image')
            with open(file_name, 'rb') as fp:
                headers = token_auth()
                headers.pop('Content-Type')
                req = requests.post(cls.resource_url(),
                                    files={'file': fp.read()},
                                    data=kwargs, headers=headers)
            if not req.ok:
                raise RuntimeError(req.content)
            else:
                log('debug', 'Successfully added file: %s' % file_name)
                return cls(req.json())
        else:
            return super(cls, File).create(**kwargs)

    def download(self, saveAt=None):
        headers = token_auth()
        headers.pop('Content-Type')
        req = requests.get(self.file_url, headers=headers, verify=False)
        if saveAt:
            with open(saveAt, 'wb') as fp:
                fp.write(req.content)

        return req.content


def apply_image_filters(filepath, filter_names=['facedetect']):
    available_filters = [x['name'] for x in get_filters()]
    if not len(filter_names):
        raise ValueError("You should specify atleast one filter among: {}",
                         available_filters)
    for name in filter_names:
        if name not in available_filters:
            raise ValueError("%s is not supported filter by Vzzual." % name)

    filters = [{'filter': name} for name in filter_names]
    req = Request.create(filters=filters)
    req.add_files(filepath, 'private')
    req.submit()
    return req, req.get_results(wait=True)
