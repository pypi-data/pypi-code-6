# coding: utf-8
import json
import time
from unittest import TestCase, main

from centrifuge.auth import decode_data, get_client_token


class FakeRequest(object):
    pass


class AuthTest(TestCase):

    def setUp(self):
        self.correct_request = FakeRequest()
        self.wrong_request = FakeRequest()
        self.wrong_request.headers = {}
        self.data = 'test'
        self.encoded_data = json.dumps(self.data)
        self.secret_key = "test"
        self.project_id = "test"
        self.user_id = "test"
        self.user_info = '{"data": "test"}'

    def test_decode_data(self):
        self.assertEqual(decode_data(self.encoded_data), self.data)

    def test_client_token(self):
        now = int(time.time())
        token_no_info = get_client_token(
            self.secret_key, self.project_id, self.user_id, str(now)
        )
        token_with_info = get_client_token(
            self.secret_key, self.project_id, self.user_id, str(now), user_info=self.user_info
        )
        self.assertTrue(token_no_info != token_with_info)

if __name__ == '__main__':
    main()
