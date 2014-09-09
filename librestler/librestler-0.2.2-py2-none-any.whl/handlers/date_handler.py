import re
from datetime import datetime
from restler.utils import isstr


class DateHandler(object):
    current = None
    types = [
        {"regex": "[0-3][0-9]/[0-3][0-9]/[0-9]{2}", "parse": "%m/%d/%y"}
    ]

    @classmethod
    def detection(cls, response, value):
        ''' DateHandler.detection:
        Tests if the value matches a recognized date string format (ISO, IETF,
        etc) so that it can then be converted into a more usable data
        structure.
        '''
        for dateset in cls.types:
            if not isstr(value):
                continue
            if re.match(dateset["regex"], value):
                cls.current = dateset["parse"]
                return True

        cls.current = None
        return False

    @classmethod
    def handler(cls, response, value):
        ''' DateHandler.handler:
        If the detection function found that the value was a date, the
        handler will be run against it.  As the detection already determined
        the parse string to use, this just needs to handle the conversion.
        '''
        if not cls.current:
            return value

        new_date = datetime.strptime(value, cls.current)
        cls.current = None

        return new_date

from restler import Response
Response.add_datatype(DateHandler.detection, DateHandler.handler)
