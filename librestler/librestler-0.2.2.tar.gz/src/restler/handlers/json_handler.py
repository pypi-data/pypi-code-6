import json


def handler(response, body):
    ''' json.handler:
    Performs a conversion from the raw string into a dictionary using the built
    in JSON library.
    '''
    return json.loads(body)

from restler import Response
Response.add_mimetype("application/json", handler)
