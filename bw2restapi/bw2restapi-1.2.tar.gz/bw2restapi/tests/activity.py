from ..activity import ActivityAPI
from .base import RestAPITestCase
from bw2data import Database, JsonWrapper


class ActivityTestCase(RestAPITestCase):
    def test_get(self):
        rv = self.app.get("/api/database/food/activity/1/")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(
            rv.content_type,
            u"application/json"
        )
        self.assertEqual(
            JsonWrapper.loads(rv.data),
            {
                u'categories': [u'stuff', u'meals'],
                u'exchanges': [{
                    u'amount': 0.5,
                    u'input': [u'food', u"2"],
                    u'type': u'technosphere',
                    u'uncertainty type': 0,
                    u'url': u'/api/database/food/activity/2/',
                    u'categories': [u'stuff', u'meals'],
                    u'location': u'CH',
                    u'unit': u'kilogram',
                    u'name': u'dinner',
                    },
                    {
                    u'amount': 0.05,
                    u'input': [u'biosphere', u"1"],
                    u'type': u'biosphere',
                    u'uncertainty type': 0,
                    u'url': u'/api/database/biosphere/activity/1/',
                    u'categories': [u'things'],
                    u'location': None,
                    u'name': u'an emission',
                    u'unit': u'kilogram',
                }],
                u'location': u'CA',
                u'name': u'lunch',
                u'unit': u'kilogram',
                u'key': [u'food', u'1'],
            }
        )

    def test_get_404(self):
        rv = self.app.get("/api/database/food/activity/1000000/")
        self.assertEqual(rv.status_code, 404)
        rv = self.app.get("/api/database/woot/activity/1/")
        self.assertEqual(rv.status_code, 404)

    def test_delete(self):
        rv = self.app.delete("/api/database/food/activity/1/")
        self.assertEqual(rv.status_code, 204)
        self.assertTrue(("food", "1") not in Database("food").load())

    def test_delete_404(self):
        rv = self.app.delete("/api/database/food/activity/1000000/")
        self.assertEqual(rv.status_code, 404)
        rv = self.app.delete("/api/database/woot/activity/1/")
        self.assertEqual(rv.status_code, 404)

    def test_put(self):
        new_ds = {
            u'categories': (u'stuff', u'meals'),
            u'exchanges': [],
            u'location': u'CA',
            u'name': u'lunch',
            u'unit': u'kilogram',
        }
        rv = self.app.put(
            "/api/database/food/activity/1/",
            data=JsonWrapper.dumps(new_ds)
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(
            Database("food").load()[("food", "1")]["exchanges"],
            []
        )

    def test_put_404(self):
        rv = self.app.put("/api/database/food/activity/1000000/", data="{}")
        self.assertEqual(rv.status_code, 404)
        rv = self.app.put("/api/database/woot/activity/1/", data="{}")
        self.assertEqual(rv.status_code, 404)

    def test_put_400(self):
        rv = self.app.put("/api/database/food/activity/1/", data="{woot}")
        self.assertEqual(rv.status_code, 400)

    def test_post(self):
        new_ds = {
            u'categories': [u'stuff', u'meals'],
            u'exchanges': [],
            u'location': u'CA',
            u'name': u'brunch!',
            u'unit': u'kilogram'
        }
        rv = self.app.post("/api/database/food/activity/1000000/", data=JsonWrapper.dumps(new_ds))
        self.assertEqual(rv.status_code, 201)
        new_ds.update({"key": ("food", "1000000")})
        self.assertEqual(
            Database("food").load()[("food", "1000000")],
            new_ds
        )

    def test_post_400(self):
        rv = self.app.post("/api/database/food/activity/1000000/", data="{woot}")
        self.assertEqual(rv.status_code, 400)

    def test_post_404(self):
        rv = self.app.post("/api/database/woot/activity/1/", data="{}")
        self.assertEqual(rv.status_code, 404)

    def test_post_409(self):
        rv = self.app.post("/api/database/food/activity/1/", data="{}")
        self.assertEqual(rv.status_code, 409)


class WaterTestCase(RestAPITestCase):
    """Test hydration, dehydration, and tuplefy methods"""
    def test_tuplefy(self):
        api = ActivityAPI()
        in_data = {'exchanges': [{'input': ["foo"]}]}
        out_data = {'exchanges': [{'input': ("foo",)}]}
        self.assertEqual(
            api._tuplefy(in_data),
            out_data
        )

    def test_hydrate_ignore_non_processes(self):
        api = ActivityAPI()
        in_data = {
            'type': 'something else',
            'exchanges': [{
                'amount': 0.5,
                'input': ('food', "2"),
                'type': 'technosphere',
                'uncertainty type': 0}]
        }
        self.assertEqual(
            sorted(api._hydrate(in_data)['exchanges'][0].keys()),
            ['amount', 'input', 'type', 'uncertainty type']
        )

    def test_hydrate(self):
        rv = self.app.get("/api/database/food/activity/1/")
        hydrated = {
            u'amount': 0.5,
            u'input': [u'food', u"2"],
            u'type': u'technosphere',
            u'uncertainty type': 0,
            u'url': u'/api/database/food/activity/2/',
            u'categories': [u'stuff', u'meals'],
            u'location': u'CH',
            u'unit': u'kilogram',
            u'name': u'dinner',
        }
        self.assertEqual(
            JsonWrapper.loads(rv.data)['exchanges'][0],
            hydrated
        )

    def test_dehydrate(self):
        api = ActivityAPI()
        in_data = {
            u'exchanges': [{
                u'amount': 0.5,
                u'input': [u'food', u"2"],
                u'type': u'technosphere',
                u'uncertainty type': 0,
                u'url': u'/api/activity/food/2/',
                u'categories': [u'stuff', u'meals'],
                u'location': u'CH',
                u'unit': u'kilogram',
                u'name': u'dinner'
            }],
        }
        self.assertEqual(
            api._dehydrate(in_data),
            {u'exchanges': [{
                u'amount': 0.5,
                u'input': [u'food', u"2"],
                u'type': u'technosphere',
                u'uncertainty type': 0,
            }]}
        )

