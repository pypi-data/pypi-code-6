from Products.Five import BrowserView
from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.common import FooterViewlet
from AccessControl import getSecurityManager
from Acquisition import ImplicitAcquisitionWrapper
from Products.CMFCore.utils import getToolByName

try:
    from collective.flowplayer.interfaces import IFlowPlayable
    FLOWPLAYER_EXISTS = True
except ImportError:
    FLOWPLAYER_EXISTS = False

class SlideshowView(ViewletBase):
    def slideshow(self, parent):
        print "get slideshow html"
        """
        Creates a slideshow with the media from parent
        """
        parentURL = parent.absolute_url()
        structure = """
        <div class="embededMediaShow">
            <a  href="%s?recursive=true">slideshow</a>
        </div>
        """%parentURL
        
        return structure

    def isVideo(self, item):
        if FLOWPLAYER_EXISTS:
            result = IFlowPlayable.providedBy(item)
        else:
            result = False
        return result

    def getMediaURL(self):
        """ finds and returns relevant leading media for the context item
        """
        item = self.context['slideshow']
        
        if(self.isVideo(item)):
            return item.absolute_url()
        
        if item.portal_type == 'Image':
            return item.absolute_url() + '/image_large'
        
        if item.portal_type == 'Link' and (item.remoteUrl.find("youtube.com") > -1 or item.remoteUrl.find("vimeo.com") > -1):
            return item.remoteUrl
        
        catalog = getToolByName(self.context, 'portal_catalog')
        plone_utils = getToolByName(self.context, 'plone_utils')
        path = '/'.join(item.getPhysicalPath())
        
        if plone_utils.isStructuralFolder(item):
            results = catalog.searchResults(path = {'query' : path,'depth' : 1 }, type = ['Image', 'File'], sort_on = 'getObjPositionInParent')
            if len(results) > 0:
                leadMedia = results[0]
                if leadMedia.portal_type == 'Image':
                    return leadMedia.getURL() + '/image_large'
                else:
                    return leadMedia.getURL()
            else:
                return ""
        else:
            return ""
    
    def slideshowInContext(self, parent, request):
        inContext = False
        if 'folder_contents' in request:
            return inContext
        try:
            inContext = 'slideshow' in parent
            return inContext
        except:
            return inContext

