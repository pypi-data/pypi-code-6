# -*- coding: utf-8 -*-
import os
import logging
import json

from OFS.Image import Image
from cStringIO import StringIO
import PIL.Image
from ZPublisher.HTTPRequest import FileUpload

from Acquisition import aq_inner
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize

TMP_FOLDER = '/'.join(INSTANCE_HOME.split('/')[:-2]) + "/var/tmp/"

try:
    os.mkdir(TMP_FOLDER)
except OSError:
    logging.info("%s already exists. No need to create." % TMP_FOLDER)

class CropPortrait(BrowserView):
    """ View where a user can crop an image and save it as his personal portrait 
    """
    
    html_template = ViewPageTemplateFile('templates/crop_portrait.pt')
    
    def __call__(self):
        """ Crop Image View. If called with parameters, image gets cropped, if not user sees view,
        where he can crop the image.
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        mt      = getToolByName(context, "portal_membership")
        action = request.get("action")

        if action == "crop":
            self.crop_image()
            uid = mt.getAuthenticatedMember().getId()
            return json.dumps(mt.getPersonalPortrait(uid).absolute_url())
            
        request.set("action", "crop_portrait")
        return self.html_template()

    
    def crop_image(self):
        """ Crops the image and sets it as Member-Portrait
        """
        context  = aq_inner(self.context)
        request = context.REQUEST
        x = int(float(request.get("x"))) 
        y = int(float(request.get("y"))) 
        w = int(float(request.get("w"))) 
        h = int(float(request.get("h")))
        mt       = getToolByName(context, "portal_membership")
        uid      = mt.getAuthenticatedMember().getId()
        tmp_file = TMP_FOLDER + uid
        
        original_file = StringIO(str(context.getImage()))
        image = PIL.Image.open(original_file)
        width, height = image.size
        size_image_preview = (768,768)
        if width > size_image_preview[0] or height > size_image_preview[1]:
            image.thumbnail(size_image_preview, PIL.Image.ANTIALIAS)
            if width > height:
                width = 768
                height = 0
            else:
                width = 0
                height = 768
            
        
        if width > height:
            scale_factor = width / 200.0
        else:
            scale_factor = height / 200.0
        w = int(w * scale_factor)
        h = int(h * scale_factor)
        x = int(x * scale_factor)
        y = int(y * scale_factor) 
        box = (x, y, x+w, y+h)
        image = image.crop(box)

        cropped_file = StringIO()
        image.save(cropped_file, "PNG", quality=88)
        cropped_file.seek(0)
        
        portrait = FileUpload(FieldStorage(cropped_file))
        mt.changeMemberPortrait(portrait, id=uid)
        cropped_file.close()

        logging.info('Portrait of user %s changed.' % uid)        
        
        return True

class FieldStorage(object):
    """ Class to fake FieldStorageObject
    """
    def __init__(self, file):
        self.file = file
        self.headers = {}
        self.filename = "portrait_photo"
