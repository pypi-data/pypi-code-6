from django.http import HttpResponse
import json


class JSONResponse(HttpResponse):

    def __init__(self, obj, status=200):
        super(JSONResponse, self).__init__(content=json.dumps(obj), content_type='application/json', status=status)