#!/usr/bin/python
# -*- coding: utf-8 -*-

# generic module for SàT frontends
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


from sat.core import constants
from sat.core.i18n import _, D_

try:
    from collections import OrderedDict  # only available from python 2.7
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError:
        pass  # libervia can not import external libraries


def getPresence():
    """We cannot do it directly in the Const class, if it is not encapsulated
    in a method we get a JS runtime SyntaxError: "missing ) in parenthetical".
    # TODO: merge this definition with those in primitivus.constants and wix.constants
    """
    try:
        presence = OrderedDict([("", _("Online")),
                                ("chat", _("Free for chat")),
                                ("away", _("Away from keyboard")),
                                ("dnd", _("Do not disturb")),
                                ("xa", _("Extended away"))])
    except TypeError:
        presence = {"": _("Online"),
                    "chat": _("Free for chat"),
                    "away": _("Away from keyboard"),
                    "dnd": _("Do not disturb"),
                    "xa": _("Extended away")
                    }
    return presence


class Const(constants.Const):

    PRESENCE = getPresence()

    # from plugin_misc_text_syntaxes
    SYNTAX_XHTML = "XHTML"
    SYNTAX_CURRENT = "@CURRENT@"
    SYNTAX_TEXT = "text"

    # XMLUI
    SAT_FORM_PREFIX = "SAT_FORM_"
    SAT_PARAM_SEPARATOR = "_XMLUI_PARAM_"  # used to have unique elements names
    XMLUI_STATUS_VALIDATED = "validated"
    XMLUI_STATUS_CANCELLED = constants.Const.XMLUI_DATA_CANCELLED

    # MUC
    ALL_OCCUPANTS = 1
    MUC_USER_STATES = {
        "active": u'✔',
        "inactive": u'☄',
        "gone": u'✈',
        "composing": u'✎',
        "paused": u"⦷"
    }

    # Roster
    GROUP_NOT_IN_ROSTER = D_('Not in roster')
