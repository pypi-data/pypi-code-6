## $Id: restwidget.py 7819 2012-03-08 22:28:46Z henrik $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""A widget that renders restructured text.
"""
from zope.component import getUtility
from zope.formlib.widget import renderElement, DisplayWidget
from waeup.kofa.utils.helpers import ReST2HTML
from waeup.kofa.interfaces import IKofaUtils


class ReSTDisplayWidget(DisplayWidget):
    """Restructured Text widget.
    """

    def __call__(self):
        """The ReSTDisplayWidget transforms a ReST text string into
        a dictionary.

        Different languages must be separated by `>>xy<<` whereas
        xy is the language code. Text parts without correct leading
        language separator - usually the first part has no language
        descriptor - are interpreted as texts in the portal's language.
        The latter can be configured in waeup.srp.utils.utils.KofaUtils.
        """
        if self._renderedValueSet():
            value = self._data
        else:
            value = self.context.default
        if value == self.context.missing_value:
            return {}
        parts = value.split('>>')
        elements = {}
        lang = getUtility(IKofaUtils).PORTAL_LANGUAGE
        for part in parts:
            if part[2:4] == u'<<':
                lang = part[0:2].lower()
                text = part[4:]
                elements[lang] = renderElement(u'div id="rest"',
                    contents=ReST2HTML(text))
            else:
                text = part
                elements[lang] = renderElement(u'div id="rest"',
                    contents=ReST2HTML(text))
        return elements
