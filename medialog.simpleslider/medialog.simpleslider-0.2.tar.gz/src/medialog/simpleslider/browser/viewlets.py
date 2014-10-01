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


class SliderViewlet(ViewletBase):
    render = ViewPageTemplateFile('simpleslider.pt')
    
    implements(ISimplesliderSettings)
    
    def update(self):
        super(SliderViewlet, self).update()
        
        #XXX the order in which these are called is important!
        self.images = self.get_images()
        self.image_urls = self.get_image_urls()
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

    def get_image_urls(self):
        if hasattr(self, 'images') and type(self.images) == list:
            return [image.absolute_url() for image in self.images]
        else:
            return []
            
    def image_size(self):
        settings = SimplesliderSettings(self.context)
        size = settings.imagesize
        image_url_end = ''
        if size != 'original':
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
});</script>""" % {
              'auto': settings.auto,
              'speed':settings.speed,
              'timeout': settings.timeout,
              'pager': settings.pager,
              'nav': settings.nav,
              'random': settings.random,
              'pause': settings.pause,
              'pausecontrols': settings.pausecontrols,
              'prevtext': settings.prevtext,
              'nexttext': settings.nexttext,
              'maxwidth': settings.maxwidth,
       }