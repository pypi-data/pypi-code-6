from zope.interface import implements, alsoProvides, noLongerProvides
from Products.Five.browser import BrowserView
from medialog.simpleslider.interfaces import ISimplesliderUtilProtected, \
    ISimplesliderUtil, ISimpleslider
from Products.CMFCore.utils import getToolByName

from plone.app.customerize import registration
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.component import getMultiAdapter

try:
    #For Zope 2.10.4
    from zope.annotation.interfaces import IAnnotations
except ImportError:
    #For Zope 2.9
    from zope.app.annotation.interfaces import IAnnotations


class SimplesliderUtilProtected(BrowserView):
    """
    a protected traverable utility for 
    enabling and disabling simpleslider
    """
    implements(ISimplesliderUtilProtected)
    def enable(self):
        utils = getToolByName(self.context, 'plone_utils')

        if not ISimpleslider.providedBy(self.context):
            alsoProvides(self.context, ISimpleslider)
            self.context.reindexObject(idxs=['object_provides'])
            utils.addPortalMessage("Simpleslider added.")
            self.request.response.redirect(self.context.absolute_url())
            
        else:  
            self.request.response.redirect(self.context.absolute_url())
        
    def disable(self):
        utils = getToolByName(self.context, 'plone_utils')
        
        if ISimpleslider.providedBy(self.context):
            noLongerProvides(self.context, ISimpleslider)
            self.context.reindexObject(idxs=['object_provides'])
            
            #now delete the annotation
            annotations = IAnnotations(self.context)
            metadata = annotations.get('medialog.simpleslider', None)
            if metadata is not None:
                del annotations['medialog.simpleslider']
                
            utils.addPortalMessage("Simpleslider removed.")
            
        self.request.response.redirect(self.context.absolute_url())
        
class SimplesliderUtil(BrowserView):
    """
    a public traverable utility that checks if it is enabled etc
    more work to do here
    """
    implements(ISimplesliderUtil)

    def enabled(self):
        return ISimpleslider.providedBy(self.context)    


    def view_enabled(self):
        utils = getToolByName(self.context, 'plone_utils')
        return True

    def should_include(self):
        return self.enabled() or self.view_enabled()
        
    
