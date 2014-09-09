#!/usr/bin/env python
#
# S3Config
# Copyright (c) 2014, Giacomo Marinangeli <jibbolo@gmail.com>
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library.

import json
import yaml

class Parser(object):
    
    class ParserError(Exception): 
        pass
    
    def __init__(self, schema="json"):
        self.schema = schema
    
    def parse(self,data):
        if self.schema == "json":
            return self.parse_json(data)
        elif self.schema == "yaml":
            return self.parse_yaml(data)
        else:
            raise ValueError("Invalid Schema: {}".format(self.schema))
    
    def parse_yaml(self,data):
        try:
            return yaml.load(data)
        except Exception, e:
            raise self.ParserError("Invalid yaml format", e)
    
    def parse_json(self,data):
        try:
            return json.loads(data)
        except Exception, e:
            raise self.ParserError("Invalid json format", e)
