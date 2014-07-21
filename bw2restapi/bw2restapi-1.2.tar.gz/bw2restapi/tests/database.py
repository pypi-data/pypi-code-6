from .base import RestAPITestCase
from bw2data import databases, JsonWrapper


class DatabaseTestCase(RestAPITestCase):
    def test_delete(self):
        self.assertTrue("food" in databases)
        rv = self.app.delete("/api/database/food/")
        self.assertEqual(rv.status_code, 204)
        self.assertFalse("food" in databases)

    def test_delete_404(self):
        self.assertEqual(
            self.app.delete("/api/database/f/").status_code,
            404
        )

    def test_get(self):
        rv = self.app.get("/api/database/food/")
        self.assertEqual(
            JsonWrapper.loads(rv.data),
            {u'depends': [], u'backend': u'json'}
        )
        self.assertEqual(
            rv.content_type,
            u"application/json"
        )
        self.assertEqual(rv.status_code, 200)

    def test_get_404(self):
        self.assertEqual(
            self.app.get("/api/database/f/").status_code,
            404
        )

    def test_post_json_db(self):
        self.assertFalse("foo" in databases)
        rv = self.app.post("/api/database/foo/", data='{"backend": "json"}')
        self.assertEqual(rv.status_code, 201)
        self.assertTrue("foo" in databases)
        self.assertEqual(
            databases["foo"],
            {u'depends': [], u'backend': u'json'}
        )

    def test_post_empty(self):
        self.assertFalse("foo" in databases)
        rv = self.app.post("/api/database/foo/")
        self.assertEqual(rv.status_code, 201)
        self.assertTrue("foo" in databases)
        self.assertEqual(
            databases["foo"],
            {u'depends': [], u'version': 0}
        )

    def test_post_default_backend(self):
        self.assertFalse("foo" in databases)
        rv = self.app.post("/api/database/foo/", data="{}")
        self.assertEqual(rv.status_code, 201)
        self.assertTrue("foo" in databases)
        self.assertEqual(
            databases["foo"],
            {u'depends': [], u'version': 0}
        )

    def test_post_400(self):
        rv = self.app.post("/api/database/foo/", data="{woot}")
        self.assertEqual(rv.status_code, 400)

    def test_post_409(self):
        rv = self.app.post("/api/database/food/")
        self.assertEqual(rv.status_code, 409)

    def test_list_databases(self):
        rv = self.app.get("/api/database/")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(
            rv.content_type,
            u"application/json"
        )
        self.assertEqual(
            JsonWrapper.loads(rv.data),
            ["biosphere", "food"]
        )

    def test_list_actvities(self):
        rv = self.app.get("/api/database/food/activity/")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(
            rv.content_type,
            u"application/json"
        )
        self.assertEqual(
            JsonWrapper.loads(rv.data),
            [
                ["food", "1"],
                ["food", "2"]
            ]
        )

    def test_list_activities_404(self):
        rv = self.app.get("/api/database/foo/activity/")
        self.assertEqual(rv.status_code, 404)
