from Acquisition import aq_inner
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements, Interface
from Products.CMFCore.utils import getToolByName

from medialog.simpleslider import simplesliderMessageFactory as _
from medialog.simpleslider.settings import SimplesliderSettings
from medialog.simpleslider.settings import ISimplesliderSettings
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter

from AccessControl import getSecurityManager

from zope.component import getMultiAdapter



class SliderViewlet(ViewletBase):
    render = ViewPageTemplateFile('simpleslider.pt')
    
    implements(ISimplesliderSettings)
    
    def update(self):
        super(SliderViewlet, self).update()
        
        #XXX the order in which these are called is important!
        self.images = self.get_images()
        self.image_list = self.get_image_list()
        self.hasImages = len(self.images) > 0
        
    def get_min_height(self):
        """
        Get the height of images.
        """
        if not self.hasImages:
            return 0
        else:
            height = self.images[0].getHeight()
            for image in self.images[1:]:
                im_height = image.getHeight()
                if im_height < height:
                    height = im_height
                    
            return height
        
    def showtitle(self):
        settings = SimplesliderSettings(self.context)
        return settings.showtitle

    def showdescription(self):
        settings = SimplesliderSettings(self.context)
        return settings.showdescription
        

    def style(self):
        """ return max, not sure if this is really needed"""
        return 'max-height:%spx' % self.get_min_height(), 
        
        
    def get_images(self):
        settings = SimplesliderSettings(self.context)
        imagepaths = settings.imagepaths
        try:
            image_folder = self.context.unrestrictedTraverse(str(imagepaths))
            return [image_folder[id] for id in image_folder.objectIds() if image_folder[id].portal_type == "Image"]
        except:
            tags = settings.tags
            sort_on = settings.sort_on
            sort_order = settings.sort_order
            catalog = api.portal.get_tool(name='portal_catalog')
            #tagged_images = catalog(portal_type=('Image', 'News Item'), Subject=tags, sort_on=sort_on, sort_order=sort_order)
            tagged_images = catalog(portal_type='Image', Subject=tags, sort_on=sort_on, sort_order=sort_order)
            return [image.getObject()for image in tagged_images]
        return []

    def get_image_list(self):
        if hasattr(self, 'images') and type(self.images) == list:
            return [{'url': image.absolute_url(), 'title': image.Title(), 'description': image.Description() } for image in self.images]
        else:
            return []
            
    def image_size(self):
        request = self.request
        settings = SimplesliderSettings(self.context)
        size = settings.imagesize
        image_url_end = ''
        try:
            active = getMultiAdapter((request.get('PUBLISHED', None), request),
                                 name='zettwerk_mobiletheming_transform') \
                ._getActive()
        except:
            active = False
        if active:
            mobilesize = settings.mobilesize
            if mobilesize and mobilesize != 'original':
                image_url_end += '//@@images/image/'
                image_url_end += mobilesize
            
        else:
            if size and size != 'original':
                image_url_end += '//@@images/image/'
                image_url_end += size
        return image_url_end
        
    def javascript(self):
        """get the settings into the javascript"""
        settings = SimplesliderSettings(self.context)
        
        return """<script>$(function () {
    $("#slider").responsiveSlides({
    maxwidth: %(maxwidth)s,
    auto: %(auto)i,
    speed: %(speed)s,
    timeout: %(timeout)s,
    pager: %(pager)i,
    nav: %(nav)i,
    pause: %(pause)i,
    pauseControls: %(pausecontrols)i,
    prevText: '%(prevtext)s',
    nextText: '%(nexttext)s',
    });
});
$(window).resize(function(){
   // Setting the heigth of the slides
   $('#slider').height($('#slider').width()*%(height)i/100);
}).resize();
</script>""" % {
              'auto'         : settings.auto,
              'speed'        : settings.speed,
              'timeout'      : settings.timeout,
              'pager'        : settings.pager,
              'nav'          : settings.nav,
              'random'       : settings.random,
              'pause'        : settings.pause,
              'pausecontrols': settings.pausecontrols,
              'prevtext'     : settings.prevtext,
              'nexttext'     : settings.nexttext,
              'maxwidth'     : settings.maxwidth,
              'height'       : settings.height,
       }