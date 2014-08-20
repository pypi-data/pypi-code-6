# -*- coding: utf-8 -*-
#
# File: MxDateTimeWidget.py
#
# Copyright (c) 2008-2014 by BlueDynamics Alliance, Bluedynamics KEG, Austria
# Generator: ArchGenXML Version 2.2 (svn)
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Georg Gogo. BERNHARD <gogo@bluedynamics.com>, Jens Klein
<jens@bluedynamics.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import TypesWidget


class MxDateTimeWidget(TypesWidget):
    """Archetypes Widget
    """

    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro': 'MxDateTimeWidget',
        'size': '30',
        'maxlength': '255',
        })

    security = ClassSecurityInfo()

registerWidget(MxDateTimeWidget,
               title='MxDateTimeWidget',
               description=('no description given'),
               used_for=('Products.Archetypes.Field.StringField',)
               )
