from api.walkscore import *
from nose.tools import *

@raises(InvalidApiKeyException)
def test_invalidapi():
    apiKey='badkey'
    walkscore = WalkScore(apiKey)

    address='somewhere'
    lat = '47.6085'
    long= '-122.3295'
    walkscore.makeRequest(address, lat, long)
