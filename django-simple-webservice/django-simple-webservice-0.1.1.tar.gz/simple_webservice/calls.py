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

"""This module contains the default calls shipped with simple-webservice and
some funtions for registering new ones

"""


#==============================================================================
# IMPORTS
#==============================================================================

import logging

from django.contrib.auth import authenticate, login as login_user
from django.contrib.sessions.models import Session

from simple_webservice import core, serializer


#==============================================================================
# LOG
#==============================================================================

# Get an instance of a logger
logger = logging.getLogger(__name__)


#==============================================================================
# REGISTER CALLS
#==============================================================================

_calls = {}


def register_call(login=False):
    """Decorator for register a new function as webservice

    :param login: If it's ``True`` the webservice the webservice require
                  authentification.
    :type login: bool

    Example
    -------

    ::

        @register_call
        def my_fancy_new_ws(*args, **kwargs):
            return {}


    """
    def _wrap(fnc):
        _calls[fnc.__name__] = {"login": login, "function": fnc}
        return fnc
    return _wrap


def execute(request, fncname, args, session_id):
    """Execute funcion (internal use

    """
    fnc_data = _calls[fncname]
    if fnc_data["login"]:
        core.user_by_session_id(session_id)
    return fnc_data["function"](request=request, session=session_id, **args)


#==============================================================================
# CALLS
#==============================================================================

@register_call()
def ping(**kwargs):
    """Always return True"""
    return {"ping": True}


@register_call()
def login(username, password, **kwargs):
    """Authentificate some user and return the session key

    """
    user = authenticate(username=username, password=password)
    request = kwargs.get("request")
    if user is not None:
        if user.is_active:
            login_user(request, user)
            session_id = request.session.session_key
            return {"session_id": session_id, "login": True}
    else:
        raise Exception("Invalid credentials")


@register_call(login=True)
def logout(session, **kwargs):
    """Delete session of logged in user

    """
    session = Session.objects.get(pk=session)
    session.delete()
    return {"login": False}


@register_call()
def check_session(session, **kwargs):
    """Verify if a session is still active"""
    try:
        Session.objects.get(pk=session)
        return {"alive": True}
    except Session.DoesNotExist:
        return {"alive": False}


@register_call()
@core.crud_function("insert")
def insert(Model, modelname, data, **kw):
    """Execute insert sql method in the given model"""
    mdl = Model.objects.create(**core.parse_data(data, Model))
    mdl.save()
    return {"pk": mdl.pk}


@register_call()
@core.crud_function("update")
def update(Model, modelname, pk, data, **kw):
    """Execute update query over given model for given primary key"""
    Model.objects.filter(pk=pk).update(**core.parse_data(data, Model))
    return {"pk": pk}


@register_call()
@core.crud_function("delete")
def delete(Model, modelname, pk, **kw):
    """Delete some object froma database with a given pk and the given model"""
    Model.objects.filter(pk=pk).delete()
    return {"pk": pk}


@register_call()
@core.crud_function("select")
def select(Model, modelname, data, **kw):
    """Excecute select statement over given model"""
    if data:
        query = Model.objects.filter(**core.parse_data(data, Model))
    else:
        query = Model.objects.all()
    return serializer.query_to_dict(query)


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
