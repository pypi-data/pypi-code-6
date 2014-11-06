from Acquisition import aq_inner
from zope.component import getUtility
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces import IPloneSiteRoot


class SlickSlideshowView(BrowserView):

    template = ViewPageTemplateFile('templates/slick_slideshow_view.pt')

    def slideshow(self, parent):
        print "Get slideshow html"
        
        """
        Creates a slideshow with the media from parent
        """

        parentURL = parent.absolute_url()
        
        mp3file = False
        mp3duration = ""
        for item in self.context["slideshow"].getFolderContents():
            if item.portal_type == "File":
                if "mp3" in item.Title:
                    mp3file = True
                    mp3path = item.getURL()
                    mp3duration = item.Description
        
        if mp3file and mp3duration != "":
            structure = """
            <div class="slick-slideshow audio" data-audio='%s' data-audio-duration='%s'>
            <a href="%s?recursive=true" id='slide-get-content'></a>    
            </div>
            """%(mp3path, mp3duration, parentURL)
        else:
            structure = """
            <div class="slick-slideshow" data-audio='' data-audio-duration=''>
            <a href="%s?recursive=true" id='slide-get-content'></a>    
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

