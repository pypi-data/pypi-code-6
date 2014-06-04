#
# Copyright 2013, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import warnings

from couchbase.tests.base import ConnectionTestCase
from couchbase.exceptions import NotFoundError, TemporaryFailError
import couchbase._libcouchbase as LCB

class DupKeyTestCase(ConnectionTestCase):
    def setUp(self):
        super(DupKeyTestCase, self).setUp()

    def _assertWarned(self, wlog):
        mcount = 0
        while wlog:
            w = wlog.pop()
            self.assertEqual(w.category, RuntimeWarning)
            print(w.message)
            mcount += 1

        self.assertTrue(mcount)
        warnings.resetwarnings()

    def test_duplicate_keys(self):
        with warnings.catch_warnings(record=True) as wlog:
            self.cb._privflags |= LCB.PYCBC_CONN_F_WARNEXPLICIT
            warnings.resetwarnings()

            meths = (self.cb.get_multi,
                     self.cb.delete_multi,
                     self.cb.incr_multi,
                     self.cb.decr_multi)

            for m in meths:
                print(m.__name__)
                try:
                    m(("foo", "foo"))
                except NotFoundError:
                    pass
                self._assertWarned(wlog)


            try:
                self.cb.lock_multi(("foo", "foo"), ttl=5)
            except NotFoundError:
                pass
            self._assertWarned(wlog)

            ktmp = self.gen_key("duplicate_keys")
            rv = self.cb.set(ktmp, "value")

            try:
                self.cb.unlock_multi((rv, rv))
            except (NotFoundError, TemporaryFailError):
                pass
            self._assertWarned(wlog)
