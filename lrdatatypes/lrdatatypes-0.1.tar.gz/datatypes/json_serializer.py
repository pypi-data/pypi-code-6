import simplejson as json
from flask import request


def from_json(string):
    return json.loads(string)


def to_json(dictionary):
    return json.dumps(dictionary)


def parse_json_from_request():
    return json.loads(request.data)