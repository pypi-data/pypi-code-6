from base import Base

class Catalog(Base):
	
    def __init__(self, apikey, response_format):
        Base.__init__(self, apikey, response_format)
        self.url = "/".join((self.ENDPOINT, response_format, "catalog"))
              	
    def search(self, string, **params):
        payload  = self.build_payload(params, { 'search': string })
        response = self.get(self.url, params=payload)
        return response['Products']['List']