from .client import Client
from .datastream import Datastream
from .datapoint import Datapoint
from .access_token import AccessToken


class Dotide(object):

    """Dotide."""

    def __init__(self,
                 database,
                 client_id=None,
                 client_secret=None,
                 access_token=None):
        self.client = Client(database,
                             client_id=client_id,
                             client_secret=client_secret,
                             access_token=access_token)
        self.datastreams = Datastream(self.client)
        self.datapoints = Datapoint(self.client)
        self.access_tokens = AccessToken(self.client)
