#!/usr/bin/env python
from .api import Api
import json
import sys
import pprint


def main():

    cfg = json.loads(open("dunbits.json").read())

    api = Api(key=cfg['api_key'])

    token = api.get_token(token=sys.argv[1])
    pprint.pprint(token)

if __name__ == '__main__':
    main()
