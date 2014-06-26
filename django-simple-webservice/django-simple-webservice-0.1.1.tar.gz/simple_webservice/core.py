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

"""Core functionalities of dsws

"""


#==============================================================================
# IMPORTS
#==============================================================================

import logging
import datetime
import functools

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils.importlib import import_module
from django.db import models


#==============================================================================
# LOG
#==============================================================================

log = logging.getLogger('simplewebservice')


#==============================================================================
# CONF
#==============================================================================

LOADING_SIMPLE_WEBSERVICE = False

REGISTERED_MODELS = {"select": {}, "insert": {}, "delete": {}, "update": {}}

PARSERS = {
    models.DateTimeField: lambda x, f: (
        datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
        if isinstance(x, basestring) else x
    ),
    models.TimeField: lambda x, f: (
        datetime.datetime.strptime(x, "%H:%M:%S.%f").time()
        if isinstance(x, basestring) else x
    ),
    models.DateField: lambda x, f: (
        datetime.datetime.strptime(x, "%Y-%m-%d").date()
        if isinstance(x, basestring) else x
    ),
    models.ForeignKey: lambda x, f: f.related_field.model.objects.get(pk=x)
}


DEFAULT_PARSER = lambda x, f: x


#==============================================================================
# FUNCTIONS
#==============================================================================

def webservice_autodiscover():
    """
    Auto-discover INSTALLED_APPS webservices.py modules and fail silently when
    not present. NOTE: autodiscover was inspired/copied from
    django.contrib.admin autodiscover

    """
    global LOADING_SIMPLE_WEBSERVICE
    if LOADING_SIMPLE_WEBSERVICE:
        return
    LOADING_SIMPLE_WEBSERVICE = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:

        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('webservices', app_path)
        except ImportError:
            continue

        import_module("%s.webservices" % app)

    LOADING_SIMPLE_WEBSERVICE = False


def user_by_session_id(session_id):
    """Utility for recover an User from their session id"""
    session = Session.objects.get(pk=session_id)
    return User.objects.get(pk=session.get_decoded()['_auth_user_id'])


def register_model(Model, select=False, insert=False,
                   update=False, delete=False, login=False):
    """Register a model for access for traditional queries
    (insert/select/update/delete)

    You can configure your model for allow execute the the query with
    authentification

    For example, if you want to allow a webservice for execute a select method
    as annonymous but the insert and delete as registered
    user with the command:

    ::

        register.model(auth.models.User, select=True)
        register.model(auth.models.User, insert=True, delete=True, login=True)

    """
    name = "{}.{}".format(Model._meta.app_label, Model.__name__)
    if select:
        REGISTERED_MODELS["select"][name] = Model, login
    if insert:
        REGISTERED_MODELS["insert"][name] = Model, login
    if delete:
        REGISTERED_MODELS["delete"][name] = Model, login
    if update:
        REGISTERED_MODELS["update"][name] = Model, login


def model_by_op(model_name, op):
    """Retrieve model by query name"""
    try:
        return REGISTERED_MODELS[op][model_name]
    except:
        raise ValueError(
            "Model '{}' do not allowed for {}".format(model_name, op)
        )


def parse_data(data, mdl):
    """Convert raw json query into model like objects"""
    fields = dict((f.name, f) for f in mdl._meta.fields)
    parsed = {}
    for k, v in data.items():
        field = fields.get(k)
        if not field:
            field = fields[k.rsplit("__", 1)[0]]
        parsed[k] = PARSERS.get(type(field), DEFAULT_PARSER)(v, field)
    return parsed


def crud_function(op):
    """Wraps functionas crus one"""
    def _inner(fnc):
        @functools.wraps(fnc)
        def _wrap(modelname, *a, **kw):
            Model, login = model_by_op(modelname, op)
            if login:
                user_by_session_id(kw["session"])
            return fnc(Model, modelname, *a, **kw)
        return _wrap
    return _inner


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
