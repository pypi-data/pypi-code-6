from base import Base

class Catalog(Base):
	
    def __init__(self, apikey):
        Base.__init__(self, apikey)
        self.url = "/".join((self.ENDPOINT, "catalog"))
              	
    def search(self, string, **params):
        payload  = self.build_payload(params, { 'search': string })
        response = self.get(self.url, params=payload)
        return response['Products']['List']