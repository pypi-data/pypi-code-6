# encoding: utf-8
# Copyright 2009–2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

import unittest2 as unittest
from edrnsite.portlets.testing import EDRNSITE_PORTLETS_INTEGRATION_TESTING
from edrnsite.portlets.portlets import dmccrss
from plone.portlets.interfaces import IPortletType, IPortletAssignment, IPortletDataProvider, IPortletManager, IPortletRenderer
from zope.component import getUtility, getMultiAdapter
from Products.GenericSetup.utils import _getDottedName

class PortletTest(unittest.TestCase):
    layer = EDRNSITE_PORTLETS_INTEGRATION_TESTING
    def setUp(self):
        super(PortletTest, self).setUp()
        self.portal = self.layer['portal']
        self.folder = self.portal['folder']
    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name=u'edrnsite.portlets.DMCCRSS')
        self.assertEquals(portlet.addview, u'edrnsite.portlets.DMCCRSS')
    def testRegisteredInterfaces(self):
        portlet = getUtility(IPortletType, name=u'edrnsite.portlets.DMCCRSS')
        registeredInterfaces = [_getDottedName(i) for i in portlet.for_]
        registeredInterfaces.sort()
        self.assertEquals(['plone.app.portlets.interfaces.IColumn', 'plone.app.portlets.interfaces.IDashboard'],
            registeredInterfaces)
    def testInterfaces(self):
        portlet = dmccrss.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet))
    def testInvokeAddview(self):
        portlet = getUtility(IPortletType, name=u'edrnsite.portlets.DMCCRSS')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={})
        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], dmccrss.Assignment))
    def testRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = dmccrss.Assignment()
        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, dmccrss.Renderer))
        
class RendererTest(unittest.TestCase):
    layer = EDRNSITE_PORTLETS_INTEGRATION_TESTING
    def setUp(self):
        super(RendererTest, self).setUp()
        self.portal = self.layer['portal']
        self.folder = self.portal['folder']
    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = assignment or dmccrss.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
    def testRSSItems(self):
        r = self.renderer(assignment=dmccrss.Assignment())
        self.assertEquals(False, r.enabled)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
