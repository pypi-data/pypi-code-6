#!/usr/bin/python
# -*- coding: utf-8 -*-

# Libervia: a SAT frontend
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014 Jérôme Poisson (goffi@goffi.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sat.core.i18n import D_
from sat_frontends import constants


class Const(constants.Const):

    # Frontend parameters
    COMPOSITION_KEY = D_("Composition")
    ENABLE_UNIBOX_PARAM = D_("Enable unibox")

    # MISC
    PASSWORD_MIN_LENGTH = 6  # for new account creation

    # HTTP REQUEST RESULT VALUES
    PROFILE_AUTH_ERROR = 'PROFILE AUTH ERROR'
    XMPP_AUTH_ERROR = 'XMPP AUTH ERROR'
    ALREADY_WAITING = 'ALREADY WAITING'
    SESSION_ACTIVE = 'SESSION ACTIVE'
    PROFILE_LOGGED = 'LOGGED'
    ALREADY_EXISTS = 'ALREADY EXISTS'
    REGISTRATION_SUCCEED = 'REGISTRATION'
    INTERNAL_ERROR = 'INTERNAL ERROR'
    BAD_REQUEST = 'BAD REQUEST'
    NO_REPLY = 'NO REPLY'
    NOT_ALLOWED = 'NOT ALLOWED'
    UPLOAD_OK = 'UPLOAD OK'
    UPLOAD_KO = 'UPLOAD KO'
    UNKNOWN_ERROR = 'UNMANAGED FAULT STRING (%s)'

    # PATHS
    AVATARS_DIR = "avatars/"

    # Default avatar
    DEFAULT_AVATAR = "/media/misc/default_avatar.png"
