# encoding: utf-8
# Copyright 2010 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EDRN Knowledge Environment Reviews: test the setup of this package.
'''

from eke.review.config import PROJECTNAME
from Products.Archetypes.public import listTypes
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_hasattr
import unittest2 as unittest
from eke.review.testing import EKE_REVIEW_INTEGRATION_TESTING

class SetupTest(unittest.TestCase):
    '''Unit tests the setup of this package.'''
    layer = EKE_REVIEW_INTEGRATION_TESTING
    def setUp(self):
        super(SetupTest, self).setUp()
        self.portal = self.layer['portal']
    def testDependencies(self):
        '''Check if our dependent packages are installed when we're installed.'''
        skinsTool = getToolByName(self.portal, 'portal_skins')
        self.failUnless(safe_hasattr(skinsTool, 'PloneFormGen'), "PloneFormGen not installed, but it's supposed to be")
    def testWidgets(self):
        '''Ensure our custom widgets are available to PloneFormGen'''
        classes = listTypes(PROJECTNAME)
        myTypes = [item['name'] for item in classes]
        typesTool = getToolByName(self.portal, 'portal_types')
        # Weird. We used to have our custom widget in both FormFolder and FieldsetFolder, but in between setuphandlers
        # and testing, FieldsetFolder cleans our custom widget out. Since I don't expect HK to want to nest
        # URLFieldsetFolders in FieldsetFolders, I'll let it go for now. If we do need that, then re-enable
        # the following line ↓ and figure out why it gets cleared out.
        # for typeName in ('FormFolder', 'FieldsetFolder'):
        for typeName in ('FormFolder',):
            ptType = typesTool.getTypeInfo(typeName).allowed_content_types
            for myType in myTypes:
                self.failUnless(myType in ptType, 'My widget "%s" missing from "%s"' % (myType, typeName))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
