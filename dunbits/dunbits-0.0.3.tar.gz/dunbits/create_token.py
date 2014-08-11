#!/usr/bin/env python
from .api import Api
import pprint
import json


def main():

    cfg = json.loads(open("dunbits.json").read())

    api = Api()
    content = "test_content"
    widget = cfg['widget']

    token = api.create_token(widget=widget, content=content)
    pprint.pprint(token)


if __name__ == '__main__':
    main()
