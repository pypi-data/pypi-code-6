# Copyright 2014 Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the 'License'); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import base64
import random
import string
from tempest import exceptions

from tempest.api.keyvalue.rest_base.base import MagnetoDBTestCase
from tempest.common.utils.data_utils import rand_name
from tempest.test import attr


class MagnetoDBPutItemTest(MagnetoDBTestCase):

    @classmethod
    def setUpClass(cls):
        super(MagnetoDBPutItemTest, cls).setUpClass()

    def random_name(self, length):
        return ''.join(random.choice(string.lowercase + string.digits)
                       for i in range(length))

    @attr(type='PI-1')
    def test_put_item_insert_one_attribute(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{'attribute_name': 'message', 'attribute_type': 'S'}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": 'message_text'}
        }
        put_resp = self.client.put_item(self.table_name, item)
        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"S": 'message_text'}},
                                        consistent_read=True)
        self.assertEqual(get_resp[1]['item']['message'],
                         {'S': 'message_text'})

    @attr(type='PI-2')
    def test_put_item_insert_few_attributes(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{'attribute_name': 'message', 'attribute_type': 'S'},
             {'attribute_name': 'author', 'attribute_type': 'S'}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": 'message_text'},
            "author": {"S": "Bob"}
        }
        put_resp = self.client.put_item(self.table_name, item)
        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"S": 'message_text'}},
                                        consistent_read=True)
        self.assertEqual(get_resp[1]['item']['author'],
                         {'S': 'Bob'})

    @attr(type='PI-3')
    def test_put_item_update_one_attribute(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{'attribute_name': 'message', 'attribute_type': 'S'}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": 'message_text'},
            "author": {"S": "Bob"},
        }
        new_item = {
            "message": {"S": "message_text"},
            "author": {"S": "Alice"},
        }
        expected = {
            "author": {
                "exists": "true",
                "value": {"S": "Bob"}
            }
        }
        put_resp = self.client.put_item(self.table_name, item)
        self.assertEqual(put_resp[1], {})
        put_resp = self.client.put_item(self.table_name,
                                        new_item, expected)
        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"S": 'message_text'}},
                                        consistent_read=True)
        self.assertEqual(get_resp[1]['item']['author'],
                         {'S': 'Alice'})

    @attr(type='PI-4')
    def test_put_item_update_few_attributes(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{'attribute_name': 'message', 'attribute_type': 'S'}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": 'message_text'},
            "author": {"S": "Bob"},
            "id": {"N": "1"}
        }
        new_item = {
            "message": {"S": "message_text"},
            "author": {"S": "Alice"},
            "id": {"N": "2"}
        }
        expected = {
            "author": {
                "exists": "true",
                "value": {"S": "Bob"}
            }
        }
        put_resp = self.client.put_item(self.table_name, item)
        self.assertEqual(put_resp[1], {})
        put_resp = self.client.put_item(self.table_name,
                                        new_item, expected)
        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"S": 'message_text'}},
                                        consistent_read=True)
        self.assertEqual(get_resp[1]['item']['author'],
                         {'S': 'Alice'})
        self.assertEqual(get_resp[1]['item']['id'],
                         {'N': '2'})

    @attr(type='PI-5')
    def test_put_item_update_few_lines_without_exist_state(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{'attribute_name': 'message', 'attribute_type': 'S'}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": 'message_text'},
            "author": {"S": "Bob"},
            "id": {"N": "1"}
        }
        new_item = {
            "message": {"S": "message_text"},
            "author": {"S": "Alice"},
            "id": {"N": "2"}
        }
        expected = {
            "author": {
                "value": {"S": "Bob"}
            }
        }
        put_resp = self.client.put_item(self.table_name, item)
        self.assertEqual(put_resp[1], {})
        put_resp = self.client.put_item(self.table_name,
                                        new_item, expected)
        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"S": 'message_text'}},
                                        consistent_read=True)
        self.assertEqual(get_resp[1]['item']['author'],
                         {'S': 'Alice'})
        self.assertEqual(get_resp[1]['item']['id'],
                         {'N': '2'})

    @attr(type='PI-10')
    def test_put_item_with_few_attributes_of_type_b(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{"attribute_name": "message", "attribute_type": "B"}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        blob = base64.b64encode('fblob')
        item = {
            "message": {"B": "qazw"},
            "author": {"B": "qwer"},
            "blob": {"B": blob}
        }
        put_resp = self.client.put_item(self.table_name, item)
        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"B": "qazw"}},
                                        consistent_read=True)
        self.assertEqual(get_resp[1]["item"]["message"], {"B": "qazw"})
        self.assertEqual(get_resp[1]["item"]["author"], {"B": "qwer"})
        self.assertEqual(get_resp[1]['item']["blob"], {"B": blob})

    @attr(type='PI-11')
    def test_put_item_with_few_attributes_of_type_bs(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{"attribute_name": "message", "attribute_type": "S"}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": "message"},
            "author": {"BS": ["qqqq", "wwww"]},
            "blob": {"BS": ["rrrr", "tttt"]}
        }
        put_resp = self.client.put_item(self.table_name, item)
        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"S": "message"}},
                                        consistent_read=True)
        self.assertEqual(set(get_resp[1]["item"]["author"]["BS"]),
                         {"qqqq", "wwww"})
        self.assertEqual(set(get_resp[1]['item']["blob"]["BS"]),
                         {"rrrr", "tttt"})

    @attr(type='PI-12')
    def test_put_item_with_few_attributes_of_type_n(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{"attribute_name": "message", "attribute_type": "N"}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"N": "1"},
            "author": {"N": "2"},
            "blob": {"N": "3"}
        }
        put_resp = self.client.put_item(self.table_name, item)
        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"N": "1"}},
                                        consistent_read=True)
        self.assertEqual(get_resp[1]["item"]["message"], {"N": "1"})
        self.assertEqual(get_resp[1]["item"]["author"], {"N": "2"})
        self.assertEqual(get_resp[1]['item']["blob"], {"N": "3"})

    @attr(type='PI-13')
    def test_put_item_with_few_attributes_of_type_ns(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{"attribute_name": "message", "attribute_type": "S"}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": "message"},
            "id": {"NS": ["1", "2"]},
            "other": {"NS": ["3", "4"]}
        }
        put_resp = self.client.put_item(self.table_name, item)
        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"S": "message"}},
                                        consistent_read=True)
        self.assertEqual(set(get_resp[1]["item"]["id"]["NS"]),
                         {"1", "2"})
        self.assertEqual(set(get_resp[1]['item']["other"]["NS"]),
                         {"3", "4"})

    @attr(type='PI-14')
    def test_put_item_with_few_attributes_of_type_ss(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{"attribute_name": "message", "attribute_type": "S"}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": "message"},
            "author": {"SS": ["eeee", "qqqq", "nnnn"]},
            "other": {"SS": ["rrrr", "tttt"]}
        }
        put_resp = self.client.put_item(self.table_name, item)
        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"S": "message"}},
                                        consistent_read=True)
        self.assertEqual(set(get_resp[1]["item"]["author"]["SS"]),
                         {"eeee", "nnnn", "qqqq"})
        self.assertEqual(set(get_resp[1]['item']["other"]["SS"]),
                         {"rrrr", "tttt"})

    @attr(type='PI-15')
    def test_put_item_with_attributes_of_all_types(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{"attribute_name": "message", "attribute_type": "S"}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": "message"},
            "author": {"SS": ["eeee", "qqqq", "nnnn"]},
            "id": {"N": "1"},
            "ids": {"NS": ["2", "3"]},
            "blob": {"B": "blob"},
            "blobs": {"BS": ["qqqq", "wwww", "eeee"]}
        }
        put_resp = self.client.put_item(self.table_name, item)
        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"S": "message"}},
                                        consistent_read=True)
        self.assertEqual(set(get_resp[1]["item"]["author"]["SS"]),
                         {"eeee", "nnnn", "qqqq"})
        self.assertEqual(get_resp[1]["item"]["id"], {"N": "1"})
        self.assertEqual(set(get_resp[1]['item']["ids"]["NS"]),
                         {"2", "3"})
        self.assertEqual(get_resp[1]["item"]["blob"], {"B": "blob"})
        self.assertEqual(set(get_resp[1]['item']["blobs"]["BS"]),
                         {"qqqq", "eeee", "wwww"})

    @attr(type='PI-50')
    def test_put_item_exist_state_by_default(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{'attribute_name': 'message', 'attribute_type': 'S'}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": 'message_text'},
            "author": {"S": "Bob"},
            "id": {"N": "1"}
        }
        new_item = {
            "message": {"S": "message_text"},
            "author": {"S": "Alice"},
            "id": {"N": "2"}
        }
        expected = {
            "author": {
                "value": {"S": "Bob"}
            }
        }
        put_resp = self.client.put_item(self.table_name, item)
        self.assertEqual(put_resp[1], {})
        put_resp = self.client.put_item(self.table_name,
                                        new_item, expected)
        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"S": 'message_text'}},
                                        consistent_read=True)
        self.assertEqual(get_resp[1]['item']['author'],
                         {'S': 'Alice'})
        self.assertEqual(get_resp[1]['item']['id'],
                         {'N': '2'})

    @attr(type='PI-51')
    def test_put_item_exists_true(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{'attribute_name': 'message', 'attribute_type': 'S'}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": 'message_text'},
            "author": {"S": "Bob"},
            "id": {"N": "1"}
        }
        new_item = {
            "message": {"S": "message_text"},
            "author": {"S": "Alice"},
            "id": {"N": "2"}
        }
        expected = {
            "author": {
                "exists": "true",
                "value": {"S": "Bob"}
            }
        }
        put_resp = self.client.put_item(self.table_name, item)
        self.assertEqual(put_resp[1], {})
        put_resp = self.client.put_item(self.table_name,
                                        new_item, expected)
        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"S": 'message_text'}},
                                        consistent_read=True)
        self.assertEqual(get_resp[1]['item']['author'],
                         {'S': 'Alice'})
        self.assertEqual(get_resp[1]['item']['id'],
                         {'N': '2'})

    @attr(type='PI-80')
    def test_put_item_with_returned_none(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{'attribute_name': 'message', 'attribute_type': 'S'}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": 'message_text'},
            "authors": {"SS": ["Alice", "Bob"]},
            "others": {"SS": ["qqqq", "wwww"]}
        }
        new_item = {
            "message": {"S": "message_text"},
            "authors": {"SS": ["Kris", "Rob"]},
            "others": {"SS": ["zzzz", "xxxx"]}
        }
        self.client.put_item(self.table_name, item)
        put_resp = self.client.put_item(self.table_name,
                                        new_item,
                                        None,
                                        0,
                                        "NONE")
        self.assertEqual(put_resp[1], {})

    @attr(type=['PI-85', 'negative'])
    def test_put_item_with_returned_empty_string(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{'attribute_name': 'message', 'attribute_type': 'S'}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": 'message_text'},
            "authors": {"SS": ["Alice", "Bob"]},
            "others": {"SS": ["qqqq", "wwww"]}
        }
        with self.assertRaises(exceptions.BadRequest) as raises_cm:
            self.client.put_item(self.table_name, item, None, 0, "")

        exception = raises_cm.exception
        self.assertIn("Bad request", exception._error_string)
        self.assertIn("ValidationError", exception._error_string)
        self.assertIn("u\'\' is not one of [\'NONE\', \'ALL_OLD\']",
                      exception._error_string)

    @attr(type=['PI-86', 'negative'])
    def test_put_item_with_wrong_string_in_returned_attribute(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{'attribute_name': 'message', 'attribute_type': 'S'}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": 'message_text'},
            "authors": {"SS": ["Alice", "Bob"]},
            "others": {"SS": ["qqqq", "wwww"]}
        }
        with self.assertRaises(exceptions.BadRequest) as raises_cm:
            self.client.put_item(self.table_name,
                                 item,
                                 None,
                                 0,
                                 "wrong_string")

        exception = raises_cm.exception
        self.assertIn("Bad request", exception._error_string)
        self.assertIn("ValidationError", exception._error_string)
        self.assertIn("u\'wrong_string\' is not one of [\'NONE\',"
                      " \'ALL_OLD\']",
                      exception._error_string)

    @attr(type='PI-87')
    def test_put_item_with_returned_is_empty(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{'attribute_name': 'message', 'attribute_type': 'S'}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": 'message_text'},
            "authors": {"SS": ["Alice", "Bob"]},
            "others": {"SS": ["qqqq", "wwww"]}
        }
        new_item = {
            "message": {"S": "message_text"},
            "authors": {"SS": ["Kris", "Rob"]},
            "others": {"SS": ["zzzz", "xxxx"]}
        }
        self.client.put_item(self.table_name, item)
        put_resp = self.client.put_item(self.table_name,
                                        new_item,
                                        None,
                                        0,
                                        None)
        self.assertEqual(put_resp[1], {})

    @attr(type=['PI-101', 'negative'])
    def test_put_item_in_nonexistent_table(self):
        item = {
            "message": {"S": 'message_text'},
            "author": {"S": "Bob"}
        }
        with self.assertRaises(exceptions.NotFound) as raises_cm:
            self.client.put_item("nonexistenttable", item)

        exception = raises_cm.exception
        self.assertIn("Not Found", exception._error_string)
        self.assertIn("The resource could not be found.",
                      exception._error_string)
        self.assertIn("Table 'nonexistenttable' does not exist",
                      exception._error_string)

    @attr(type='PI-110')
    def test_put_item_with_existent_key(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{'attribute_name': 'message', 'attribute_type': 'S'}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": 'message_text'},
            "author": {"SS": ["Alice", "Bob"]},
            "other": {"SS": ["qqqq", "wwww"]}
        }
        new_item = {
            "message": {"S": "message_text"},
            "author": {"S": "Kris"},
            "other": {"S": "zzzz"}
        }
        put_resp = self.client.put_item(self.table_name, item)
        self.assertEqual(put_resp[1], {})

        put_resp = self.client.put_item(self.table_name, new_item)
        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"S": "message_text"}},
                                        consistent_read=True)
        self.assertEqual(get_resp[1]["item"]["author"], {"S": "Kris"})
        self.assertEqual(get_resp[1]['item']["other"], {"S": "zzzz"})

    @attr(type='PI-112')
    def test_put_item_duplicate_key_name(self):
        self.table_name = rand_name().replace('-', '')
        self._create_test_table(
            [{'attribute_name': 'message', 'attribute_type': 'S'}],
            self.table_name,
            [{'attribute_name': 'message', 'key_type': 'HASH'}],
            wait_for_active=True)
        item = {
            "message": {"S": "message_text_1"},
            "message": {"S": "message_text_2"}
        }
        put_resp = self.client.put_item(self.table_name, item)

        self.assertEqual(put_resp[1], {})
        get_resp = self.client.get_item(self.table_name,
                                        {"message": {"S": "message_text_2"}},
                                        consistent_read=True)
        self.assertEqual(get_resp[1]["item"]["message"],
                         {"S": "message_text_2"})
