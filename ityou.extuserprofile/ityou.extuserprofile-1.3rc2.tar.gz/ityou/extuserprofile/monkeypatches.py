# -*- coding: utf-8 -*-

from OFS.Image import Image
from Acquisition import aq_inner, aq_parent, aq_base

from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.MemberDataTool import MemberData as BaseMemberData
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.permissions import ManageUsers
from Products.PluggableAuthService.interfaces.authservice import IPluggableAuthService
from Products.PlonePAS.utils import getCharset
from plone.memoize.instance import memoize

from zope.site.hooks import getSite

from Products.PlonePAS.utils import scale_image
import hashlib

from OFS.Image import Image
from cStringIO import StringIO
import PIL.Image
from browser.crop_portrait import FieldStorage
from ZPublisher.HTTPRequest import FileUpload

from dbapi import DBApi

dbapi = DBApi()

_marker = object()


def patchedChangeMemberPortrait(self, portrait, id=None):
    """update the portait of a member.

    Modified from CMFPlone version to URL-quote the member id.
    
    How to get the Portraits in different sizes?
    ----------------------------------------------
    call:     mt.getPersonalPortrait(user_id, size='thumb')
    Available square sizes : 
              thumb, tile, pico icon micro
              4/3-Sizes:
              large, oversized
    no size: get Plone default size 
    """
    safe_id = self._getSafeMemberId(id)
    authenticated_id = self.getAuthenticatedMember().getId()  
    user = dbapi.getExtendedProfile(id)
    
    if not safe_id:
        # The default is to change your own portrait.
        safe_id = authenticated_id
    if authenticated_id and safe_id != authenticated_id:
        # Only Managers can change portraits of others.
        if not _checkPermission(ManageUsers, self):
            raise Unauthorized 
    if portrait and portrait.filename:
        membertool = getToolByName(self, 'portal_memberdata')        
        
        # Modified Code - variable sizes  >>>>>>  
        square_sizes = {
            "thumb"   : (128,128),
            "tile"    : (64,64),
            "pico"    : (48,48),
            "icon"    : (32,32),
            "micro"   : (16,16)
            }
        sizes = {
            'large'     : (150,200),
            'oversized' : (225,300)
            } 
        original = 'original'
        # ---
        
        original_file = StringIO(str(portrait.read()))
        portrait.seek(0)
        image = PIL.Image.open(original_file)
        
        width = image.size[0]
        height = image.size[1]        
        if width > height:
            new_width = height
            new_height = height
        else:
            new_height = width
            new_width = width
        
        # make square ----
        x = ( width - new_width ) / 3
        y = ( height - new_height ) / 3       
        box = (x, y, x+new_width, y+new_height)
        image = image.crop(box)
        
        cropped_file = StringIO()
        image.save(cropped_file, "PNG", quality=88)
        cropped_file.seek(0)
        
        square_portrait = FileUpload(FieldStorage(cropped_file))
        
        _scale_image(self, safe_id, square_sizes, square_portrait)
        _scale_image(self, safe_id, sizes, portrait)
        
        # save original
        md5 = _get_hash(safe_id,original)
        original_portrait = Image(id=md5, file=portrait, title='')
        membertool._setPortrait(original_portrait, md5)
        portrait.seek(0)

        original_file.close()
        cropped_file.close()

        ## <<<< End of modified Code

        scaled, mimetype = scale_image(portrait)        
        portrait = Image(id=safe_id, file=scaled, title = '')
        membertool._setPortrait(portrait, safe_id)

        
def _scale_image(self, safe_id, sizes, image):
    """Image scaling
    """
    membertool = getToolByName(self, 'portal_memberdata')
    for size in sizes.keys():
        scaled, mimetype = scale_image(image, sizes[size])
        md5 = _get_hash(safe_id,size)
        scaled_portrait = Image(id=md5, file=scaled, title=size)
        membertool._setPortrait(scaled_portrait, md5)
        image.seek(0)
    
            
def _get_hash(safe_id, size):
    """creates a hashkey for a given size and safe_id
    """
    m = hashlib.md5()
    m.update(safe_id)
    m.update(size)
    return m.hexdigest()
    
    


def patchedGetPersonalPortrait(self, id=None, verifyPermission=0, size=None):
    """Return a members personal portait.

    Modified from CMFPlone version to URL-quote the member id.
    """

    if size:
        default_portrait = 'defaultUser-' + size + '.png'
    else:
        default_portrait = 'defaultUser.png'

    if id is None:
        portal = getToolByName(self, 'portal_url').getPortalObject()
        return getattr(portal, default_portrait, None)
    
    site = getSite()
    
    safe_id = self._getSafeMemberId(id)
    membertool   = getToolByName(self, 'portal_memberdata')

    if not safe_id:
        safe_id = self.getAuthenticatedMember().getId()

    auth_member_id = self.getAuthenticatedMember().getId()
    if self.getMemberById(safe_id) is None:
        portal = getToolByName(self, 'portal_url').getPortalObject()
        return getattr(portal, default_portrait, None)
    #portrait_public = self.getMemberById(safe_id).getProperty("public_portrait")

    # Modified Code - variable sizes >>>>>
    if not size:
        portrait = membertool._getPortrait(safe_id)
    else:
        m = hashlib.md5()
        m.update(safe_id)
        m.update(size)
        md5 = m.hexdigest()
        portrait = membertool._getPortrait(md5)
    # <<<<<< End of Modified Code
        
    if isinstance(portrait, str):
        portrait = None
    if portrait is not None:
        if verifyPermission and not _checkPermission('View', portrait):
            # Don't return the portrait if the user can't get to it
            portrait = None
    if portrait is None:
        portal = getToolByName(self, 'portal_url').getPortalObject()
        portrait = getattr(portal, default_portrait, None)

    return portrait
