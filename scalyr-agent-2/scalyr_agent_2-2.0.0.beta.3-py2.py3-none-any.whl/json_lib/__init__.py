# Copyright 2014, Scalyr, Inc.

r"""A lightweight JSON library used by the Scalyr agent to serialize data
for storage to disk and for sending over HTTP.

This library is used instead of python's default json library because
it supports some custom Scalyr extensions (chiefly it allows for comments
in the JSON) and the json library is not included in all versions of Python
supported by the Scalyr agent.
"""

__all__ = ['parse', 'serialize', 'JsonObject', 'JsonArray', 'JsonConversionException',
           'JsonMissingFieldException', 'JsonParseException']
__author__ = 'Steven Czerwinski <czerwin@scalyr.com>'

from scalyr_agent.json_lib.exceptions import JsonConversionException
from scalyr_agent.json_lib.exceptions import JsonMissingFieldException, JsonParseException
from scalyr_agent.json_lib.objects import JsonObject, JsonArray
from scalyr_agent.json_lib.parser import parse
from scalyr_agent.json_lib.serializer import serialize
