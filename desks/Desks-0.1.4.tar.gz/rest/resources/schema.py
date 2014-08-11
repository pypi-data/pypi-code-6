#!/usr/bin/env python

from flask import request
from flask.ext import restful
from flask.ext.restful import fields, abort
from shelves import shelves

from ..common.utils import get_shelf

class SchemaResource(restful.Resource):
    """
    This class is used to extract the schema from a shelf, can be useful
    for providing filters and stuff like that.
    """
    def get(self):
        """
        Let's get the schema of associated shelf
        """
        return get_shelf().schema()
