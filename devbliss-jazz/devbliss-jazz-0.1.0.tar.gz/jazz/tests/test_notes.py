import unittest.mock
import concurrent.futures
import tornado.process
import jazz.tests


class NotesHandlerTest(jazz.tests.TestCase):

    @unittest.mock.patch("tornado.process.Subprocess")
    def test_get(self, Subprocess):
        body = "n=73"  # A6
        process = Subprocess.return_value
        process.stdout.read_until_close.return_value = (
            concurrent.futures.Future())
        process.stdout.read_until_close.return_value.set_result(b"")
        process.proc.wait.return_value = 0
        res = self.fetch("/notes", method="POST", body=body)
        Subprocess.assert_called_once_with(
            "beep -f 1760.0", shell=True,
            stdin=tornado.process.Subprocess.STREAM,
            stdout=tornado.process.Subprocess.STREAM,
            stderr=tornado.process.Subprocess.STREAM)
        self.assertEqual(res.code, 201)

    @unittest.mock.patch("tornado.process.Subprocess")
    def test_get_internal_server_error(self, Subprocess):
        body = "n=49"
        process = Subprocess.return_value
        process.stdout.read_until_close.return_value = (
            concurrent.futures.Future())
        process.stdout.read_until_close.return_value.set_result(b"")
        process.proc.wait.return_value = 1
        res = self.fetch("/notes", method="POST", body=body)
        self.assertEqual(res.code, 500)

    @unittest.mock.patch("tornado.process.Subprocess")
    def test_get_bad_request(self, Subprocess):
        body = "n=false"
        self.assertEqual(Subprocess.mock_calls, [])
        res = self.fetch("/notes", method="POST", body=body)
        self.assertEqual(res.code, 400)
