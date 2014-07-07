# -*- coding: utf-8 -*-
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName 
from Acquisition import aq_inner

from .PyQRNative import QRCode, QRErrorCorrectLevel
from . import INSTANCE_PATH, QRCODE_LOCATION, QRCODE_RESOURCE

class QRCodeUtils:
    
    @memoize
    def create_qrcode(self,context):
        """ Creates and returns qr code
        """
        url = context.absolute_url()
        uid = context.UID()

        if len(url) < 78:
            type_number = 4
        elif len(url) < 107:
            type_number = 5
        elif len(url) < 135:
            type_number = 7
        else:
            type_number = 8

        qr = QRCode(type_number, QRErrorCorrectLevel.L)
        qr.addData(url)
        qr.make()

        im = qr.makeImage()
        im.save( '%s/%s.png' % (QRCODE_LOCATION,uid) )
        ###im.show()

        return '<img src="%s/%s.png" alt="%s" title="%s" class="image-inline img-responsive" />' % (
            QRCODE_RESOURCE,
            uid,
            context.title_or_id(),
            context.title_or_id()
            ) 
    
    def qrcode_url(self,context):
        """returns the url of the QR Code
        """
        url = context.absolute_url()
        uid = context.UID()

        url = url.replace('/view','') + '/%s/%s.png' % (QRCODE_RESOURCE, uid)
        print url
        return url

        
