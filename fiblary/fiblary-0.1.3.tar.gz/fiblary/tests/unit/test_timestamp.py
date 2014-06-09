#  Copyright 2014 Klaudiusz Staniek
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import testtools

# from fiblary.common import exceptions
from fiblary.common import timestamp


class TestUtils(testtools.TestCase):
    def test_timestamp_to_iso(self):
        self.assertEqual(
            timestamp.timestamp_to_iso(123123123),
            "1973-11-26 01:52:03")
