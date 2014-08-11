import os

from flask.ext.testing import TestCase
from trellostats.web import app

app_token = os.environ.get('TRELLOSTATS_APP_TOKEN')
app_key = os.environ.get('TRELLOSTATS_APP_KEY')


class TestCycleTimeApi(TestCase):

    def create_app(self):
        return app

    def test_400_on_root(self):
        assert self.client.get('/').status_code == 404

    def test_cant_post_on_api_endpoint(self):
        assert self.client.post('/api/v1/cycletime').status_code == 405

    def test_successful_call(self):
        happy = '/api/v1/cycletime?app_key={}&app_token={}&board_id={}&done=Done'\
                .format(app_key, app_token, 'hLeITVoI')
        response = self.client.get(happy)
        assert response.status_code == 200
        assert 'cycletime' in response.json.keys()
