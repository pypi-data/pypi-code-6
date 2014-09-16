from Products.Five import BrowserView
from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone.app.layout.viewlets.common import FooterViewlet
from AccessControl import getSecurityManager

class SlideshowView(BrowserView):
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

class CommonBrowserView(BrowserView):
    """
    Common utilities for all the other views
    """
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

class NumberOfResults(CommonBrowserView):
    """
    Called by AJAX to know how many results in the collection. Returns JSON.
    """
    def getJSON(self):
        callback = hasattr(self.request, 'callback') and 'json' + self.request['callback'] or None
        only_documented = not hasattr(self.request, 'only_documented') 
        
        result = None
        
        if self.context.portal_type == 'Collection':
            brains = self.context.queryCatalog(batch=False)
            if only_documented:
                result = []
                for res in brains:
                    if res.hasMedia:
                        result.append(res)
    
        if result is not None:
            jsonStr = json.dumps(len(result))
        else:
            jsonStr = json.dumps(result)
            
        if callback is not None:
            return callback +'(' + jsonStr + ')'
        else:
            return jsonStr 

class Footer(FooterViewlet):
    """
    helper classes for footer
    """
    def showManageButton(self):
        secman = getSecurityManager()
        if not secman.checkPermission('Portlets: Manage portlets', self.context):
            return False
        else:
            return True

