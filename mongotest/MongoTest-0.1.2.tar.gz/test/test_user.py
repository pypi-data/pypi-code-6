# -*- coding: utf-8 -*-
import unittest
import os

from pymongo import MongoClient
from mongo_test.fixtures import setup_data, oid_con, teardown_data


from mongo_test.handlers import startup, teardown, PORT


class TestUser(unittest.TestCase):

    fixture_paths = ['user_fixture.yml']

    def setUp(self):
        startup()

        conn = MongoClient(port=int(PORT))
        self.db = conn.myapp

        setup_data(self.fixture_paths, self.db)

    def test_find_user(self):
        # Fetch user by id
        user = self.db.test_users.find_one(query={'_id': oid_con(1)})
        # Check pymongo works as advertised.
        assert user
        assert user['_id'] == oid_con(1)
        assert user['username'] == 'idbentley'

    def tearDown(self):
        teardown_data(self.fixture_paths, self.db)
        teardown()
