from restler.utils import isstr


class URLHandler(object):
    @classmethod
    def detection(cls, response, value):
        ''' URLHandler.detection:
        Tests if the value matches a format that signifies it is either an
        absolute or relative path.
        '''
        if not isstr(value):
            return False

        return value.startswith('/') or \
            value.startswith(str(response.__parent__))

    @classmethod
    def handler(cls, response, value):
        ''' URLHandler.handler:
        Returns a `Route` object for the value.
        '''
        if value.startswith(str(response.__parent__)):
            value = value[len(str(response.__parent__)):]
        return response.__parent__[value]

from restler import Response
Response.add_datatype(URLHandler.detection, URLHandler.handler)
