import json


class WanticketsResponse(object):
    def __init__(self, json_data=None):
        self.success = False
        self.json_data = json_data
        self.result = {}
        if not json_data is None:
            parsed = json.loads(json_data)
            if "searchAPIResponse" in parsed:
                api_response = parsed["searchAPIResponse"]
                self.success = True \
                    if   'success' in api_response \
                    and  api_response['success'] \
                    else False
                self.message = api_response['message']
                self.result = api_response['results']