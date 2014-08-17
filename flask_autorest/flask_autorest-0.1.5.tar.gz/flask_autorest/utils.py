# -*- coding: utf-8 -*-

import json
import datetime
from flask import current_app, request


class DatetimeJSONEncoder(json.JSONEncoder):
    """可以序列化时间的JSON"""

    def default(self, o):
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        else:
            return super(DatetimeJSONEncoder, self).default(o)


def autorest_jsonify(*args, **kwargs):

    indent = None
    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] \
            and not request.is_xhr:
        indent = 2
    return current_app.response_class(json.dumps(dict(*args, **kwargs),
                                                 indent=indent, cls=DatetimeJSONEncoder),
                                      mimetype='application/json')