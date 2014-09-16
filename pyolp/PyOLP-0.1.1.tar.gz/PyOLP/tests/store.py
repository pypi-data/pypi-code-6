#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White
#                                                                              
# PyGithub is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.                                                           
#                                                                              
# PyGithub is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS   
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#                                                                      
# You should have received a copy of the GNU Lesser General Public License
# along with PyGithub. If not, see <http://www.gnu.org/licenses/>.

import unittest

from .. import PyOLP

class TestStore(unittest.TestCase):

    def setUp(self):

        self.OLP = PyOLP()

        self.store = self.OLP.get_store("1")

    def test_attributes_values(self):

        self.assertEqual(self.store.address, '4219 Agness Rd, Rogue River - Siskiyou National Forest, Agness, OR 97406, USA')
        self.assertEqual(self.store.address_raw, '04219 Agness Rd 97406')
        self.assertEqual(self.store.county, 'Curry')
        self.assertEqual(self.store.hours_raw, 'Summer: 7-8 M-Sun Winter: 9-6 M-Sun')
        self.assertEqual(self.store.id, '1')
        self.assertEqual(self.store.key, 1213)
        self.assertEqual(self.store.latitude, 42.557056)
        self.assertEqual(self.store.longitude, -124.057135)
        self.assertEqual(self.store.name, 'Agness Liquor')
        self.assertEqual(self.store.phone, '(541) 247-7233')
        self.assertEqual(self.store.resource_uri, '/api/v1/store/1/')

    def test_attributes_types(self):

        self.assertTrue(isinstance(self.store.address, (str, unicode)))
        self.assertTrue(isinstance(self.store.address_raw, (str, unicode)))
        self.assertTrue(isinstance(self.store.county, (str, unicode)))
        self.assertTrue(isinstance(self.store.hours_raw, (str, unicode)))
        self.assertTrue(isinstance(self.store.id, (str, unicode)))
        self.assertTrue(isinstance(self.store.key, (int, long)))
        self.assertTrue(isinstance(self.store.latitude, float))
        self.assertTrue(isinstance(self.store.longitude, float))
        self.assertTrue(isinstance(self.store.phone, (str, unicode)))
        self.assertTrue(isinstance(self.store.resource_uri, (str, unicode)))
