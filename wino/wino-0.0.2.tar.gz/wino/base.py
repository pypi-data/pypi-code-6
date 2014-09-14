import requests as req

class Base(object):

    ENDPOINT = 'http://services.wine.com/api/beta2/service.svc'

    def __init__(self, apikey, response_format):
        if response_format not in ['xml', 'json']:
            raise Exception("Can only respond with XML or JSON objects")
        self.apikey = { 'apikey': apikey }
        self.response_format = response_format

    def get(self, url, **params):
        payload  = self.build_payload(self.apikey, params['params'])
        response = req.get(url, params=payload)
        return response.json()

    def build_payload(self, *params):
        res = {}
        for p in params:
            res.update(p.items())
        return res