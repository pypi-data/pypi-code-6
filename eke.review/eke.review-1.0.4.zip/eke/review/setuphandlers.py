# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

import config
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_hasattr
from Products.Archetypes.public import listTypes

def importVarious(context):
    '''Miscellaneous import steps.
    '''
    if context.readDataFile('eke.review.txt') is None:
        return
    site = context.getSite()
    
    # Ensure PloneFormGen is installed
    portalSkins = getToolByName(site, 'portal_skins')
    assert safe_hasattr(portalSkins, 'PloneFormGen'), 'PloneFormGen must be installed prior to installing this package.'
    
    # Make our widget available to PloneFormGen
    classes = listTypes(config.PROJECTNAME)
    myTypes = [item['name'] for item in classes]
    portalTypes = getToolByName(site, 'portal_types')
    for typeName in ('FormFolder', 'FieldsetFolder'):
        ptType = portalTypes.getTypeInfo(typeName)
        ffact = list(ptType.allowed_content_types)
        ffact += myTypes
        ptType.manage_changeProperties(allowed_content_types=ffact)
    
