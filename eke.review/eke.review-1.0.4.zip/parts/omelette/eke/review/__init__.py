#!/usr/bin/env python
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EKE Review.
'''

from Products.Archetypes import atapi
from Products.CMFCore import utils
from zope.i18nmessageid import MessageFactory
import config

ProjectMessageFactory = MessageFactory('eke.review')

def initialize(context):
    '''Initialize when installed as a Zope 2 product.'''
    from content import urlfieldsetfolder # for side effect of AT content registration
    contentTypes, constructors, ftis = atapi.process_types(atapi.listTypes(config.PROJECTNAME), config.PROJECTNAME)
    for atype, constructor in zip(contentTypes, constructors):
        utils.ContentInit(
            '%s: %s' % (config.PROJECTNAME, atype.portal_type),
            content_types=(atype,),
            permission=config.ADD_CONTENT_PERMISSION,
            extra_constructors=(constructor,),
        ).initialize(context)
    
