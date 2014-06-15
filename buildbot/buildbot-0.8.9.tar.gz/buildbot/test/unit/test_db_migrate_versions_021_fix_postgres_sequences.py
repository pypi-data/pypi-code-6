# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

import sqlalchemy as sa

from buildbot.test.util import migration
from twisted.trial import unittest


class Migration(migration.MigrateTestMixin, unittest.TestCase):

    def setUp(self):
        return self.setUpMigrateTest()

    def tearDown(self):
        return self.tearDownMigrateTest()

    cols = [
        'buildrequests.id',
        'builds.id',
        'buildsets.id',
        'changes.changeid',
        'patches.id',
        'sourcestampsets.id',
        'sourcestamps.id',
        'objects.id',
        'users.uid',
    ]

    # tests

    def test_update(self):
        def setup_thd(conn):
            metadata = sa.MetaData()
            metadata.bind = conn

            # insert a row into each table, giving an explicit id column so
            # that the sequence is not advanced correctly, but leave no rows in
            # one table to test that corner case
            for i, col in enumerate(self.cols):
                tbl_name, col_name = col.split('.')
                tbl = sa.Table(tbl_name, metadata,
                               sa.Column(col_name, sa.Integer, primary_key=True))
                tbl.create()
                if i > 1:
                    conn.execute(tbl.insert(), {col_name: i})

        def verify_thd(conn):
            metadata = sa.MetaData()
            metadata.bind = conn

            # try inserting *without* an ID, and verify that the resulting ID
            # is as expected
            for i, col in enumerate(self.cols):
                tbl_name, col_name = col.split('.')
                tbl = sa.Table(tbl_name, metadata,
                               sa.Column(col_name, sa.Integer, primary_key=True))
                r = conn.execute(tbl.insert(), {})
                if i > 1:
                    exp = i + 1
                else:
                    exp = 1
                self.assertEqual(r.inserted_primary_key[0], exp)

        return self.do_test_migration(20, 21, setup_thd, verify_thd)
