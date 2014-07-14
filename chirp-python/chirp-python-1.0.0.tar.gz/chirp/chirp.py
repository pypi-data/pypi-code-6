from json import JSONEncoder,JSONDecoder
import json
import logging

logger = logging.getLogger(__name__)

class Chirp():

    def __init__(self,_method,_name = "",_uri = "",_port = 0 ,_protocol = "",_config = {},_sender=''):
        self.method = _method
        self.name = _name
        self.uri = _uri
        self.port = _port
        self.protocol= _protocol
        self.config = _config
        if _sender == '':
            self.sender = _name
        else:
            self.sender = _sender


class ChirpEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class ChirpDecoder(JSONDecoder):
    def decode(self, s):
        dict = json.loads(s)
        return Chirp(dict['method'],dict['name'],dict['uri'],dict['port'],dict['protocol'],dict['config'],dict['sender'])





