# -*- coding: utf-8 -*-
#
# File: MxDateRangeIndex.py
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

##code-section module-header #fill in your manual code here
from Globals import DTMLFile, InitializeClass
##/code-section module-header

import mx.DateTime
from Globals import DTMLFile, InitializeClass
from zope.interface import implements
from Products.PluginIndexes.DateRangeIndex.DateRangeIndex import DateRangeIndex
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin


class MxDateRangeIndex(DateRangeIndex):
    """
    """

    ##code-section class-header_MxDateRangeIndex #fill in your manual code here
    meta_type = "MxDateRangeIndex"
    ##/code-section class-header_MxDateRangeIndex


    def _convertDateTime( self, value ):
        if value is None:
            return value
        if type( value ) == type( '' ):
            value = mx.DateTime.DateTimeFrom( value )
        result = int(value.ticks() / 1000 / 60) # flatten to minutes
        return result


##code-section module-footer #fill in your manual code here

def initialize(context):

    context.registerClass( \
            MxDateRangeIndex,\
            permission='Add Pluggable Index', \
            constructors=(manage_addMxDateRangeIndexForm,\
                          manage_addMxDateRangeIndex),\
            icon='www/index.gif',\
            visibility=None\
            )


InitializeClass( MxDateRangeIndex )

manage_addMxDateRangeIndexForm = DTMLFile( 'dtml/addMxDateRangeIndex', globals() )
manage_indexProperties = DTMLFile( 'dtml/manageMxDateRangeIndex', globals() )

def manage_addMxDateRangeIndex(self, id, extra=None,
        REQUEST=None, RESPONSE=None, URL3=None):
    """
        Add a mx date range index to the catalog, using the incredibly icky
        double-indirection-which-hides-NOTHING.
    """
    return self.manage_addIndex(id, 'MxDateRangeIndex', extra,
        REQUEST, RESPONSE, URL3)


##/code-section module-footer


