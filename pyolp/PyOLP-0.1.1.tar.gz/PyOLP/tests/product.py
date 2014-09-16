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

class TestProduct(unittest.TestCase):

    def setUp(self):

        self.OLP = PyOLP()

        self.product = self.OLP.get_product("1")

    def test_attributes_values(self):
        
        self.assertEqual(self.product.age, 14.0)
        self.assertEqual(self.product.bottles_per_case, 6)
        self.assertEqual(self.product.code, '0103B')
        self.assertEqual(self.product.created_at, 
                datetime(2012, 9, 23, 23, 59, 50, 485635))
        self.assertEqual(self.product.description, '')
        self.assertEqual(self.product.id, '1')
        self.assertEqual(self.product.modified_at,
            datetime(2013, 12, 1, 5, 33, 33, 497373))
        self.assertEqual(self.product.on_sale, False)
        self.assertEqual(self.product.proof, 86.0)
        self.assertEqual(self.product.size, '750 ML')
        self.assertEqual(self.product.slug, '0103b')
        self.assertEqual(self.product.status, '@')
        self.assertEqual(self.product.title, 'Balvenie 14 Yr Caribbean C')

    def test_attributes_types(self):

        self.assertTrue(isinstance(self.product.age, float))
        self.assertTrue(isinstance(self.product.bottles_per_case, (int, long)))
        self.assertTrue(isinstance(self.product.code, (str, unicode)))
        self.assertTrue(isinstance(self.product.created_at, datetime))
        self.assertTrue(isinstance(self.product.description, (str, unicode)))
        self.assertTrue(isinstance(self.product.id, (str, unicode)))
        self.assertTrue(isinstance(self.product.modified_at, datetime))
        self.assertTrue(isinstance(self.product.on_sale, bool))
        self.assertTrue(isinstance(self.product.proof, float))
        self.assertTrue(isinstance(self.product.size, (str, unicode)))
        self.assertTrue(isinstance(self.product.slug, (str, unicode)))
        self.assertTrue(isinstance(self.product.status, (str, unicode)))
        self.assertTrue(isinstance(self.product.title, (str, unicode)))

