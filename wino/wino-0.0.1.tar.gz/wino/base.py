import requests as req

class Base(object):

    ENDPOINT = 'http://services.wine.com/api/beta2/service.svc/json'

    def __init__(self, apikey):
        self.apikey = { 'apikey': apikey }

    def get(self, url, **params):
        payload  = self.build_payload(self.apikey, params['params'])
        response = req.get(url, params=payload)
        return response.json()

    def build_payload(self, *params):
        res = {}
        for p in params:
            res.update(p.items())
        return res