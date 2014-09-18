# -*- coding: utf-8 -*-

from Products.Archetypes import atapi
from Products.CMFCore.utils import ContentInit
from monet.calendar.event import config
from zope.i18nmessageid import MessageFactory


eventMessageFactory = MessageFactory('monet.calendar.event')

def initialize(context):

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        ContentInit('%s: %s' % (config.PROJECTNAME, atype.portal_type),
            content_types      = (atype,),
            permission         = config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors = (constructor,),
            ).initialize(context)
