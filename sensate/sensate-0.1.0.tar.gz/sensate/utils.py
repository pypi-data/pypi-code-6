### LOGGING ACROBATICS ###

import logging
import json
import datetime

# logging to console if no other log handlers have been set up.
logger = logging.getLogger()

if logger.handlers == []:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

logger.setLevel(logging.DEBUG)

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fUTC'

# The following helper classes assist in datetime conversion between Python and JSON. 
class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()+"UTC"
        else:
            return str(obj)
        return json.JSONEncoder.default(self, obj)

class CustomJsonDecoder(json.JSONDecoder):
    def default(self, obj):
        for k, v in obj.items():
            if isinstance(v, basestring) and re.search("UTC", v):
                try:
                    obj[k] = datetime.datetime.strptime(v, DATE_FORMAT)
                except ValueError:
                    pass
        return obj

"""
def json_datetime_hook(dct):
    for k, v in dct.items():
        if isinstance(v, basestring) and re.search("UTC", v):
            try:
                dct[k] = datetime.datetime.strptime(v, DATE_FORMAT)
            except:
                pass
    return dct
"""
