try:
    import httplib
except ImportError:
    import http.client as httplib

from restler.utils import isstr
from restler.errors import ServerError, RequestError


class Response(object):
    ''' Response:
    The `Response` object is a handler+wrapper for the response document from
    the HTTP requests.  It handles trying to parse the string of data into a
    proper data structure, interpreting the status code, and organizing all of
    the information into a manageable format.
    '''
    datatypes = []
    mimetypes = {}

    def __init__(self, response, base):
        self.__base__ = response
        self.__parent__ = base
        self.url = self.__base__.geturl()
        self.headers = self.__base__.info()
        self.data = ""
        self.code = response.getcode()

        if self.code >= httplib.INTERNAL_SERVER_ERROR:
            raise ServerError(self.code, self.__base__.read())
        elif self.code >= httplib.BAD_REQUEST:
            raise RequestError(self.code, self.__base__.read())

        self.convert()
        self.data = self.parse(self.data)
        self.parse_headers()

    @classmethod
    def add_datatype(cls, datatype, handler):
        ''' (class) add_datatype:
        Takes a datatype detection function and handler function and adds it to
        the set of handlers for the various custom datatypes evaluated after
        conversion via mimetype.  The detection function takes two arguments,
        the first is the actual `Response` object (the functions are treated
        as methods of the object) and the second is the raw value (only strings
        are passed in).  The second function also takes two arguments, the
        first, again, being the `Response` object and the second being the
        value that was previously detected against.  Whatever it returns will
        be used instead of this value.
        '''
        cls.datatypes.append([datatype, handler])

    @classmethod
    def add_mimetype(cls, mime, handler):
        ''' (class) add_mimetype:
        Takes a `MIMEtype` string and a handler function and adds it to the
        lookup set for response handling.  The passed in function will take
        two parameters, the first is the actual `Response` object (the
        functions are treated as methods of the object) and the second is the
        raw body of the response.
        '''
        cls.mimetypes[mime] = handler

    def convert(self):
        ''' convert:
        Attempts to detect the MIMEtype of the response body and convert
        accordingly.
        '''
        try:
            mime = self.__base__.info().gettype()
        except AttributeError:
            mime = self.__base__.info().get_content_type()
        for mimetype, handler in self.mimetypes.items():
            if mimetype == mime:
                raw = self.__base__.read()
                if isinstance(raw, bytes):
                    raw = raw.decode("UTF-8")
                self.data = handler(self, raw)
                return

        self.data = self.__base__.read()

    def parse(self, data):
        ''' parse:
        Loops over the data, looking for string values that can be parsed into
        rich data structures (think 2012-12-24 becomes a `datetime` object).
        '''
        # handle is just a function that is mapped against a list
        def handle(val):
            for datatype in self.datatypes:
                if datatype[0](self, val):
                    return datatype[1](self, val)

            return val

        if isinstance(data, list):
            return list(map(self.parse, data))
        elif not isinstance(data, dict):
            return handle(data)

        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = self.parse(value)
                continue

            if isinstance(value, list):
                data[key] = map(self.parse, value)

            if not isstr(value):
                continue

            data[key] = handle(value)

        return data

    def parse_headers(self):
        ''' parse_headers:
        Traverses the headers of the response and sets them in the `headers`
        dictionary of the object.  Any handlers set for a header type will be
        run against a header if it exists.
        '''
        if 'Link' in self.headers:
            self.__link_header()

    def __link_header(self):
        ''' (private) link_header:
        If the `Link` header is set in the response, the values will be parsed
        and appropriate methods will be added for the relative locations.
        '''
        links_raw = self.__base__.headers['Link'].split(',')
        links = {}
        for link in links_raw:
            info_raw = link.split(';')
            info = {'url': info_raw[0].strip(' <>')}
            for i in info_raw[1:]:
                i = i.split('=')
                info[i[0]] = i[1]

            links[info['rel']] = info

    def __repr__(self):
        return "Response: " + self.url

    def __str__(self):
        return self.__base__.read()

    def __nonzero__(self):
        return self.code < httplib.BAD_REQUEST
