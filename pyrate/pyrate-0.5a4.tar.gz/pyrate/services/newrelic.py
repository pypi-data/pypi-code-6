#todo: reenable after debugging
#from pyrate.main import Pyrate
import json
from main import Pyrate


class NewrelicPyrate(Pyrate):
    # This variable must be set on instantiation
    api_key = ''

    http_methods = ['GET']
    default_http_method = http_methods[0]
    response_formats = ['json']
    default_body_content = {}
    auth_type = 'API_KEY'
    #connection_check_method = ['POST', 'helper/ping', 'msg', "Everything's Chimpy!"]
    connection_check_method = []
    send_json = True

    def __init__(self, apikey, default_http_method=None, default_return_format=None):
        super(NewrelicPyrate, self).__init__()
        self.api_key = apikey
        self.base_url = 'https://api.newrelic.com/api/v2/'
        self.default_header_content = {
            'X-Api-Key': self.api_key
        }

        if default_http_method:
            self.default_http_method = default_http_method

        if default_return_format or default_return_format == '':
            self.default_response_format = default_return_format



if __name__ == "__main__":
    h = NewrelicPyrate('4f68ecbfe3d6f56f74fa44de3329ec5005c3ad26949136d')

    # check if the connection works
    #h.check_connection()

    # direct api call
    print(h.default_header_content)
    print(h.do('applications', http_method="GET", headers="X-Api-Key :4f68ecbfe3d6f56f74fa44de3329ec5005c3ad26949136d"))