# -*- coding: utf-8 -*-
#
# File: MxDateTimeField.py
#
# Copyright (c) 2008 by BlueDynamics Alliance, Bluedynamics KEG, Austria
# Generator: ArchGenXML Version 2.2 (svn)
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Georg Gogo. BERNHARD <gogo@bluedynamics.com>, Jens Klein
<jens@bluedynamics.com>"""
__docformat__ = 'plaintext'

from .MxDateTimeWidget import MxDateTimeWidget
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Field import ObjectField
from Products.Archetypes.Field import registerField
from mx.DateTime import DateTimeFrom
from mx.DateTime import DateTimeType
from types import StringTypes


class MxDateTimeField(ObjectField):
    """Archetypes Field
    """

    _properties = ObjectField._properties.copy()
    _properties.update({
        'type': 'mxdatetimefield',
        'widget': MxDateTimeWidget,
        })

    security = ClassSecurityInfo()
    security.declarePrivate('set')
    security.declarePrivate('get')

    def set(self, instance, value, **kwargs):
        """
        Check if value is an actual date/time value. If not, attempt
        to convert it to one; otherwise, set to None. Assign all
        properties passed as kwargs to object.
        """
        if not value:
            value = None

        if type(value) in StringTypes:
            value = DateTimeFrom(value)

        if value and type(value) != DateTimeType:
            raise ValueError("Argument to MxDateTimeField must be either "
                             "a string or a MxDateTime object, but "
                             "got: %s" % repr(value))

        ObjectField.set(self, instance, value, **kwargs)

registerField(MxDateTimeField,
              title='MxDateTimeField',
              description='')
