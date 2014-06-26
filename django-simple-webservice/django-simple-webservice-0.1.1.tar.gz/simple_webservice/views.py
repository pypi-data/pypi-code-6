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

"""Django views

"""


#==============================================================================
# IMPORTS
#==============================================================================

import json
import traceback
import sys
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db import transaction

from simple_webservice import calls


#==============================================================================
# LOG
#==============================================================================

log = logging.getLogger('simplewebservice')


#==============================================================================
# VIEWS
#==============================================================================

@csrf_exempt
@require_POST
@transaction.atomic
def call(request):
    """
    query = {
        "id": arbitrario
        "name": nombre de funcion a ejecutar
        "args": argumen tos de la funcion
        "session": token de la funcion
    }

    return = {
        "id": igual que el id que fue
        "error": bool
        "error_msg": si error es true
        "stacktrace": string
        "response": puede ser none o el resultado
    }

    """
    qid, qname, args = None, None, None
    error, response, error_msg, stacktrace = False, None, "", ""
    try:
        data = None
        if "query" in request.POST:
            data = json.loads(request.POST["query"])
        else:
            data = json.loads(request.body)
        qid = data["id"]
        qname = data["name"]
        qargs = data["args"]
        session_id = data.get("session")
        response = calls.execute(request, qname, qargs, session_id)
    except Exception as err:
        error = True
        error_msg = unicode(err)
        if settings.DEBUG:
            stacktrace = u"".join(
                traceback.format_exception(*sys.exc_info())
            )
            print stacktrace

    data = {"id": qid, "error": error, "error_msg": error_msg,
            "stacktrace": stacktrace, "response": response}
    sdata = json.dumps(data)
    log.debug(sdata)
    return HttpResponse(sdata, content_type='application/json')


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
