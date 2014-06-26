#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django-simple-webservice
# Copyright (c) 2014, Liricus, All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.


#==============================================================================
# DOCS
#==============================================================================

"""Django app for simple creation webservices json-rpc like

"""


#==============================================================================
# IMPORTS
#==============================================================================

from simple_webservice.core import webservice_autodiscover
from simple_webservice.core import register_model
from simple_webservice.core import user_by_session_id
from simple_webservice.core import parse_data
from simple_webservice.calls import register_call
from simple_webservice.serializer import query_to_dict, model_to_dict


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
