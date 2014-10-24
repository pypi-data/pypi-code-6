# coding:utf-8
from scalr_client_core import api


class TestAPIClient(api.APIClient):
    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []
        super(TestAPIClient, self).__init__("", "", "", "")

    def _request(self, url):
        self.requests.append(url)
        return self.responses.pop(0)