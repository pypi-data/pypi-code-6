# -*- coding: utf-8 -*-
"""
    tlutil.json
"""

import errors
import simplejson

from datetime import datetime, date


__all__ = [
    "jsonify", "JSONEncoder"
]


class JSONEncoder(object):
    """自定义JSON格式化
    """
    def default(self, obj):
        return jsonify(obj)


def _default(obj):
    if isinstance(obj, errors.AppError):
        return dict(code=obj.code, message=obj.message)
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, date):
        return obj.strftime("%Y-%m-%d")
    raise TypeError("%r is not JSON serializable" % obj)


def jsonify(args):
    return simplejson.dumps(args, default=_default)
