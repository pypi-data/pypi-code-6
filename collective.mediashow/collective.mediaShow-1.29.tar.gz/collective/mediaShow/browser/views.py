from Products.Five import BrowserView
from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.common import FooterViewlet
from AccessControl import getSecurityManager
from Acquisition import ImplicitAcquisitionWrapper

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
    
    def slideshowInContext(self, parent, request):
        inContext = False
        if 'folder_contents' in request:
            return inContext
        try:
            inContext = 'slideshow' in parent
            return inContext
        except:
            return inContext

