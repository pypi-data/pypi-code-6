from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
     
from Products.CMFCore.interfaces._content import IFolderish

class AstreamViewlet(ViewletBase):
    
    render = ViewPageTemplateFile('browser/templates/astream_viewlet.pt')

    def available(self):
        context = aq_inner(self.context)
        ###print "context.allow_discussion", getattr(context, 'allow_discussion', False)
        try:
            if getattr(context, 'allow_discussion', False) and not IFolderish.providedBy(context):
                return True
            else:
                return False
        except:
            return False
