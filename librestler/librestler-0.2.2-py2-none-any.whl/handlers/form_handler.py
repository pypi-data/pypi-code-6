try:
    from urlparse import parse_qs
except ImportError:
    from urllib.parse import parse_qs


def handler(response, body):
    ''' form.handler:
    Performs a conversion from the raw string into a dictionary using the built
    in urlparsing library.
    '''
    data = parse_qs(body)
    for key, value in data.items():
        if len(value) == 1:
            data[key] = value[0]

    return data

from restler import Response
Response.add_mimetype("application/x-www-form-urlencoded", handler)
