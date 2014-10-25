import jazz.tests


class IndexHandlerTest(jazz.tests.TestCase):

    def test_get(self):
        res = self.fetch("/", follow_redirects=False)
        self.assertEqual(res.code, 200)
