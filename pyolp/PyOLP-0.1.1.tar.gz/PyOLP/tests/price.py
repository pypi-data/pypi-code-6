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

from datetime import datetime

class TestPrice(unittest.TestCase):

    def setUp(self):

        self.OLP = PyOLP()

        self.price = self.OLP.get_price("1")

    def test_attributes_values(self):

        self.assertEqual(self.price.amount, 64.95)
        self.assertEqual(self.price.created_at, 
                datetime(2012, 9, 23, 23, 59, 50, 493148))
        self.assertEqual(self.price.effective_date,
                datetime(2012, 10, 1, 0, 0))
        self.assertEqual(self.price.id, '1')
        self.assertEqual(self.price.modified_at,
                datetime(2012, 9, 23, 23, 59, 50, 493166))
        self.assertEqual(self.price.resource_uri, 
                '/api/v1/price/1/')

    def test_attributes_types(self):

        self.assertTrue(isinstance(self.price.amount, float))
        self.assertTrue(isinstance(self.price.created_at, datetime))
        self.assertTrue(isinstance(self.price.effective_date, datetime))
        self.assertTrue(isinstance(self.price.id, (str, unicode)))
        self.assertTrue(isinstance(self.price.modified_at, datetime))
        self.assertTrue(isinstance(self.price.resource_uri, (str, unicode)))
