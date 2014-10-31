#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A few checks at the UTFVP database.
"""

import os, sys
import unittest
import xbob.db.utfvp

class UTFVPDatabaseTest(unittest.TestCase):
  """Performs various tests on the UTFVP database."""

  def test01_clients(self):
    # test whether the correct number of clients is returned
    db = xbob.db.utfvp.Database()

    self.assertEqual(len(db.groups()), 2)
    self.assertEqual(len(db.protocols()), 2)
    self.assertEqual(len(db.protocol_names()), 2)
    self.assertEqual(len(db.purposes()), 3)

    self.assertEqual(len(db.clients()), 360)
    self.assertEqual(len(db.clients(protocol='master')), 354)
    self.assertEqual(len(db.clients(protocol='paper')), 360)
    self.assertEqual(len(db.client_ids()), 360)
    self.assertEqual(len(db.client_ids(protocol='master')), 354)
    self.assertEqual(len(db.client_ids(protocol='paper')), 360)

    self.assertEqual(len(db.models()), 1300)
    self.assertEqual(len(db.models(protocol='master')), 1276)
    self.assertEqual(len(db.models(protocol='paper')), 1300)
    self.assertEqual(len(db.model_ids()), 1300)
    self.assertEqual(len(db.model_ids(protocol='master')), 1276)
    self.assertEqual(len(db.model_ids(protocol='paper')), 1300)


  def test02_objects(self):
    # tests if the right number of File objects is returned
    db = xbob.db.utfvp.Database()

    self.assertEqual(len(db.objects()), 1440)
    self.assertEqual(len(db.objects(groups='world')), 140)
    self.assertEqual(len(db.objects(groups='dev')), 1300)

    self.assertEqual(len(db.objects(protocol='master')), 1416)
    self.assertEqual(len(db.objects(protocol='master', groups='world')), 140)
    self.assertEqual(len(db.objects(protocol='master', groups='dev')), 1276)

    self.assertEqual(len(db.objects(protocol='paper')), 1440)
    self.assertEqual(len(db.objects(protocol='paper', groups='world')), 140)
    self.assertEqual(len(db.objects(protocol='paper', groups='dev')), 1300)

    self.assertEqual(len(db.objects(protocol='master', groups='dev', model_ids=('1_2_3',))), 1276)
    self.assertEqual(len(db.objects(protocol='master', groups='dev', model_ids=('1_2_3',), purposes='enrol')), 1)
    self.assertEqual(len(db.objects(protocol='master', groups='dev', model_ids=('1_2_3',), purposes='probe')), 1275)
    self.assertEqual(len(db.objects(protocol='master', groups='dev', model_ids=('1_2_3',), purposes='probe', classes='client')), 3)
    self.assertEqual(len(db.objects(protocol='master', groups='dev', model_ids=('1_2_3',), purposes='probe', classes='impostor')), 1272)

    self.assertEqual(len(db.objects(protocol='paper', groups='dev', model_ids=('1_2_3',))), 1300)
    self.assertEqual(len(db.objects(protocol='paper', groups='dev', model_ids=('1_2_3',), purposes='enrol')), 1)
    self.assertEqual(len(db.objects(protocol='paper', groups='dev', model_ids=('1_2_3',), purposes='probe')), 1299)
    self.assertEqual(len(db.objects(protocol='paper', groups='dev', model_ids=('1_2_3',), purposes='probe', classes='client')), 3)
    self.assertEqual(len(db.objects(protocol='paper', groups='dev', model_ids=('1_2_3',), purposes='probe', classes='impostor')), 1296)

  def test03_driver_api(self):

    from bob.db.script.dbmanage import main
    self.assertEqual(main('utfvp dumplist --self-test'.split()), 0)
    self.assertEqual(main('utfvp dumplist --protocol=master --class=client --group=dev --purpose=enrol --model=1_2_3 --self-test'.split()), 0)
    self.assertEqual(main('utfvp checkfiles --self-test'.split()), 0)
    self.assertEqual(main('utfvp reverse 0001/0001_1_1_120509-135315 --self-test'.split()), 0)
    self.assertEqual(main('utfvp path 37 --self-test'.split()), 0)

