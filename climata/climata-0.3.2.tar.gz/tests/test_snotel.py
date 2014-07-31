import unittest
from .base import ClimataTestCase
from climata.snotel import StationIO, StationDailyDataIO, RegionDailyDataIO, ElementIO

from climata.snotel import server
"""
# SOAPpy doesn't work well with httpretty; run tests against the live server.
try:
    can_access = server.areYouThere()
except:
    can_access = False
  
@unittest.skipUnless(can_access, "server not online")
class SnotelTestCase(unittest.TestCase):
    def test_station(self):
        data = StationIO(
            basin='18010201',
        )
        self.assertGreater(len(data), 0)
        item = data[0]
#self.assertHasFields(item, ("station_nm", "dec_lat_va", "dec_long_va"))
        """
