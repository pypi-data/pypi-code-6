# -*- coding: utf-8 -*-
#
# File: MxDateIndex.py
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
import mx
from Globals import DTMLFile, InitializeClass
##/code-section module-header

import mx.DateTime
from Globals import DTMLFile
from zope.interface import implements
from Products.PluginIndexes.DateIndex.DateIndex import DateIndex
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin


class MxDateIndex(DateIndex):
    """
    """

    ##code-section class-header_MxDateIndex #fill in your manual code here
    meta_type = "MxDateIndex"
    ##/code-section class-header_MxDateIndex


    def _convert( self, value, default=None ) :
        """Convert Date/Time value to our internal representation"""

        if type(value) == type('') :
            value = mx.DateTime.DateTimeFrom(value)

        if isinstance( value, mx.DateTime.mxDateTime.DateTimeType ):
            t_tup = value.tuple()
        else:
            return default

        yr = t_tup[0]
        mo = t_tup[1]
        dy = t_tup[2]
        hr = t_tup[3]
        mn = t_tup[4]

        t_val = ( ( ( ( yr * 12 + mo ) * 31 + dy ) * 24 + hr ) * 60 + mn )

        return t_val


##code-section module-footer #fill in your manual code here

InitializeClass( MxDateIndex )

def initialize(context):

    context.registerClass( \
            MxDateIndex,\
            permission='Add Pluggable Index', \
            constructors=(manage_addMxDateIndexForm,\
                          manage_addMxDateIndex),\
            icon='www/index.gif',\
            visibility=None\
            )

manage_addMxDateIndexForm = DTMLFile( 'dtml/addMxDateIndex', globals() )

def manage_addMxDateIndex( self, id, REQUEST=None, RESPONSE=None, URL3=None):
    """Add a MxDate index"""
    return self.manage_addIndex(id, 'MxDateIndex', extra=None, \
                    REQUEST=REQUEST, RESPONSE=RESPONSE, URL1=URL3)
##/code-section module-footer


