from testtools import TestCase, ExpectedException
from mock import Mock, patch
from itertools import repeat
from . import makeprefs
from lacore.exceptions import (ApiAuthException, ApiErrorException,
                               UploadEmptyError)
from lacore.async import block
from twisted.internet import defer
from itertools import imap
import json


class ApiTest(TestCase):
    def setUp(self):
        super(ApiTest, self).setUp()
        self.prefs = makeprefs()['api']

    def tearDown(self):
        super(ApiTest, self).tearDown()

    def _makeit(self, *args, **kw):
        from lacore.api import Api
        return Api(*args, **kw)

    def _mocksessions(self, rsps):
        return Mock(**rsps)

    def _json_request(self, url, mock_call):
        args, kwargs = mock_call.call_args
        headers = kwargs['headers']
        self.assertEqual('application/json', headers['content-type'])
        self.assertEqual(url, args[0])
        return kwargs['data']

    def test_api(self):
        assert self._makeit(self.prefs, Mock())

    def test_api_root(self):
        r = json.loads(LA_ENDPOINTS_RESPONSE)
        s = self._mocksessions({'get.return_value': defer.succeed(r)})
        api = self._makeit(self.prefs, session=s)
        self.assertEqual(r, api.root)

    def test_no_capsules(self):
        caps = json.loads(LA_EMPTY_COLLECTION)
        r = [defer.succeed(json.loads(LA_ENDPOINTS_RESPONSE)),
             defer.succeed(caps)]
        s = self._mocksessions({'get.side_effect': r})
        api = self._makeit(self.prefs, session=s)
        capsules = list(api.capsules())
        self.assertEqual(len(capsules), 0)

    def simple_session(self, response):
        j = map(defer.succeed,
                map(json.loads, [LA_ENDPOINTS_RESPONSE, LA_CAPSULES_RESPONSE]))
        return self._mocksessions({'get.side_effect': j})

    def capsule_session(self):
        return self.simple_session(LA_CAPSULES_RESPONSE)

    def test_capsules(self):
        api = self._makeit(self.prefs, session=self.capsule_session())
        capsules = list(api.capsules())
        self.assertEqual(len(capsules), 2)

    def test_capsule_ids(self):
        api = self._makeit(self.prefs, session=self.capsule_session())
        ids = api.capsule_ids()
        self.assertTrue(2 in ids)
        self.assertTrue(3 in ids)

    def test_capsule_ids_size(self):
        api = self._makeit(self.prefs, session=self.capsule_session())
        ids = api.capsule_ids(150).iterkeys()
        self.assertTrue(2 in ids)
        self.assertTrue(3 not in ids)

    def test_no_archives(self):
        arcs = json.loads(LA_EMPTY_COLLECTION)
        r = [defer.succeed(json.loads(LA_ENDPOINTS_RESPONSE)),
             defer.succeed(arcs)]
        s = self._mocksessions({'get.side_effect': r})
        api = self._makeit(self.prefs, session=s)
        archives = list(api.archives())
        self.assertEqual(len(archives), 0)

    def archive_session(self):
        return self.simple_session(LA_ARCHIVES_RESPONSE)

    def test_archives(self):
        api = self._makeit(self.prefs, session=self.archive_session())
        archives = list(api.archives())
        self.assertEqual(len(archives), 2)

    def test_unauthorized(self):
        r = [defer.succeed(json.loads(LA_ENDPOINTS_RESPONSE)),
             defer.fail(ApiAuthException())]
        s = self._mocksessions({'get.side_effect': r})
        api = self._makeit(self.prefs, session=s)
        with ExpectedException(ApiAuthException):
            list(api.capsules())

    def test_status_start(self):
        _gets = map(defer.succeed,
                    map(json.loads,
                        [LA_ENDPOINTS_RESPONSE, LA_CAPSULES_RESPONSE]))
        _posts = imap(defer.succeed, repeat(json.loads(LA_UPLOAD_RESPONSE)))
        s = self._mocksessions({'get.side_effect': _gets,
                                'post.side_effect': _posts})
        api = self._makeit(self.prefs, session=s)
        state = Mock(uri=None, sandbox=False,
                     capsule={'resource_uri': '/1'})
        op = api.upload(Mock(title='',
                             description='',
                             meta=Mock(size=1)), state)
        self.assertEqual(None, op.uri)
        block(lambda: op.status)()
        uri = 'http://baz.com/api/v1/upload/1/'
        self.assertEqual(uri, op.uri)
        self.assertFalse(op.sandbox)

    def test_status_start_sandbox(self):
        _gets = map(defer.succeed,
                    map(json.loads,
                        [LA_ENDPOINTS_RESPONSE, LA_CAPSULES_RESPONSE]))
        _posts = imap(defer.succeed, repeat(json.loads(LA_SANDBOX_RESPONSE)))
        s = self._mocksessions({'get.side_effect': _gets,
                                'post.side_effect': _posts})
        api = self._makeit(self.prefs, session=s)
        state = Mock(uri=None, sandbox=True,
                     capsule={'resource_uri': '/1'})
        op = api.upload(Mock(title='',
                             description='',
                             meta=Mock(size=1)), state)
        self.assertEqual(None, op.uri)
        block(lambda: op.status)()
        uri = 'http://baz.com/api/v1/upload/1/'
        self.assertEqual(uri, op.uri)
        self.assertTrue(op.sandbox)

    @patch('lacore.api.getLogger', create=True)
    def test_status_error(self, log):
        _gets = map(defer.succeed,
                    map(json.loads,
                        [LA_ENDPOINTS_RESPONSE, LA_CAPSULES_RESPONSE,
                         LA_UPLOAD_RESPONSE]))
        _gets.append(defer.fail(ApiErrorException()))
        _posts = imap(defer.succeed, repeat(json.loads(LA_UPLOAD_RESPONSE)))
        s = self._mocksessions({'get.side_effect': _gets,
                                'post.side_effect': _posts})
        api = self._makeit(self.prefs, session=s)
        state = Mock(uri=None, sandbox=False,
                     capsule={'resource_uri': '/1'})
        op = api.upload(Mock(title='',
                             description='',
                             meta=Mock(size=1)), state)
        block(lambda: op.status)()
        block(lambda: op.status)()
        block(lambda: op.status)()
        log.return_value.debug.return_value = None
        self.assertRaises(ApiErrorException, block(lambda: op.status))
        log.assert_called_with()
        log.return_value.debug.assert_called_with(
            'Exception while getting status', exc_info=True)

    def test_finalize_empty(self):
        api = self._makeit(self.prefs)
        op = api.upload(Mock(), Mock(uri=None, capsule={'resource_uri': '/1'}))
        self.assertRaises(UploadEmptyError, op.finalize)


LA_UPLOAD_RESPONSE_TMPL = """{{
    "id": 1,
    "capsule": "/api/v1/capsule/1/",
    "title": "foo",
    "description": "foo",
    "resource_uri": "/api/v1/upload/1/",
    "status": "pending",
    "token_access_key": "XXXXXXXXXXXXXXXXXXXX",
    "token_secret_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "token_session": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "token_expiration": "",
    "token_uid": "arn:aws:iam::XXXXXXXXXXXX:user/sts-test-dummy",
    "bucket": "lastage",
    "prefix": "prefix",
    "sandbox": {sandbox}
}}
"""


LA_UPLOAD_RESPONSE = LA_UPLOAD_RESPONSE_TMPL.format(sandbox='false')


LA_SANDBOX_RESPONSE = LA_UPLOAD_RESPONSE_TMPL.format(sandbox='true')


LA_ENDPOINTS_RESPONSE = """{
  "account": {
     "list_endpoint": "/api/v1/account/",
     "schema": "/api/v1/account/schema/"
  },
  "archive": {
     "list_endpoint": "/api/v1/archive/",
     "schema": "/api/v1/archive/schema/"
  },
  "capsule": {
     "list_endpoint": "/api/v1/capsule/",
     "schema": "/api/v1/capsule/schema/"
  },
  "upload": {
     "list_endpoint": "/api/v1/upload/",
     "schema": "/api/v1/upload/schema/"
  }
}
"""

LA_CAPSULES_RESPONSE = """{
  "meta": {
     "limit": 20,
     "next": null,
     "offset": 0,
     "previous": null,
     "total_count": 2
  },
  "objects": [
     {
         "created": "2013-06-07T10:45:01",
         "id": 3,
         "resource_uri": "/api/v1/capsule/3/",
         "title": "Photos",
         "size": 1000,
         "remaining": 100,
         "user": "/api/v1/user/3/"
      },
      {
          "created": "2013-06-07T10:44:38",
          "id": 2,
          "resource_uri": "/api/v1/capsule/2/",
          "title": "Stuff",
          "size": 1000,
          "remaining": 200,
          "user": "/api/v1/user/2/"
       }
    ]
}"""

LA_EMPTY_COLLECTION = """{
  "meta": {
     "limit": 20,
     "next": null,
     "offset": 0,
     "previous": null,
     "total_count": 0
  },
  "objects": []
}"""

LA_ARCHIVES_RESPONSE = """{
   "objects" : [
      {
         "capsule" : "/api/v1/capsule/3/",
         "description" : "man",
         "size" : "1310288",
         "key" : "120-NV5DVV",
         "created" : "2014-04-10T06:19Z",
         "resource_uri" : "/api/v1/archive/120-NV5DVV/",
         "title" : "yo",
         "expires" : "2015-01-21T23:59Z"
      },
      {
         "capsule" : "/api/v1/capsule/2/",
         "description" : "baba",
         "size" : "3150096",
         "key" : "109-PW9SLN",
         "created" : "2014-04-05T16:04Z",
         "resource_uri" : "/api/v1/archive/109-PW9SLN/",
         "title" : "yoyo",
         "expires" : "2015-01-21T23:59Z"
      }
   ],
   "meta" : {
      "previous" : null,
      "next" : "/api/v1/archive/?limit=20&offset=20",
      "limit" : 20,
      "total_count" : 2,
      "offset" : 0
   }
}"""
