# -*- coding: utf-8 -*-
## -----------------------------------------------------------------
## Copyright (C)2013 ITYOU - www.ityou.de - support@ityou.de
## -----------------------------------------------------------------
"""
This module contains all views of ityou.dragdrop
"""
import logging
import json
from exceptions import KeyError

from Acquisition import aq_inner, aq_parent

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.uuid.utils import uuidToObject

from AccessControl import getSecurityManager
from Products.CMFCore.permissions import AddPortalContent, DeleteObjects

from ..dbapi import DBApi
from .. import isProductAvailable
from .. import _
from .. import TRASH_FOLDER
from plone import api

DB = DBApi()
     
class AjaxDragDropView(BrowserView):
    """Ajax View which handles DragDrop events
    """

    def __call__(self):
        """ Checks the action given in the request and calls the 
        resulting function
        Returns JSON
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        
        action = request.get('action')
        mt = getToolByName(context, "portal_membership")
        ut = Utils()

        if mt.isAnonymousUser():
            return ut.jsonResponse(context,False)


        ##DEBUG
        #print "_______________________"
        #print "ACTION: ", action
        #print "UID:    ", request.get('uid')
       
        if not action:
            res = None

        # dragdrop objects
        elif action == 'add_dragdrop_object':
            res = self._addObjectInDragDropBox()
        elif action == 'remove_dragdrop_object':
            res = self._removeObjectInDragDropBox()
        elif action == 'get_dragdrop_objects':
            res = self._getObjectsFromDragDropBox()

        # copy / move / delete plone objects
        elif action == 'copy_object':
            res = self._copyOrMoveObject(copy = True)
        elif action == 'move_object':
            res = self._copyOrMoveObject(move = True)
        elif action == 'move_to_trash':
            res = self._moveObjectToTrash()

        else:
            res = False
        
        return ut.jsonResponse(context, res)

    
    def _addObjectInDragDropBox(self):
        """ ADD OBJECT TO DRAGDROP BOX (not to folder)
        Checks the authenticated user id.
        Then calls the DBApi addObject function with the checked user id and
        uid.
        Returns the value returned by DBApi function as jSON (True / False).
        """
        context =     aq_inner(self.context)
        request =     context.REQUEST
        mt =          getToolByName(context, 'portal_membership')
        auth_member = mt.getAuthenticatedMember()

        if api.user.is_anonymous():
            return False

        user_id = auth_member.getId()
        uid = request.get('uid')
        if not uid:
            logging.warning('_addObjectInDragDropBox: Got no uid!')

        return DB.addObject(user_id, uid)


    def _removeObjectInDragDropBox(self):
        """ REMOVES OBJECT FROM DRAGDROP-BOX (not from Folder)
        Checks the authenticated user id.
        Then calls the DBApi addObject function with the checked user id and
        uid.
        Returns the value returned by DBApi function as jSON (True / False).
        """
        context =   aq_inner(self.context)
        request =   context.REQUEST
        mt =        getToolByName(context, 'portal_membership')

        auth_member = mt.getAuthenticatedMember()
        if api.user.is_anonymous():
            return False

        user_id = auth_member.getId()
        uid = request.get('uid')
        if not uid:
            logging.warning('_removeObjectInDragDropBox: Got no uid!')
            return False
        return DB.removeObject(user_id, uid)


    def _getObjectsFromDragDropBox(self):
        """ Get objects for the current user
        Returns: [{
                uid,
                id,
                title,
                url,
                portal_type,
                thumbnail_url
            }, ... ]
        """
        context =   aq_inner(self.context)
        mt =        getToolByName(context, 'portal_membership')
        rt =        getToolByName(self, 'reference_catalog')

        auth_member = mt.getAuthenticatedMember()

        if api.user.is_anonymous():
            return False

        user_id = auth_member.getId()
        uids = DB.getObjects(user_id)

        objects = []
        for uid in uids:
            obj = uuidToObject(uid)
            if obj:

                object = {}
                object["uid"] = uid
                object["id"] = obj.getId()
                object["title"] = obj.title_or_id()
                object["description"] = obj.Description()
                object["portal_type"] = obj.portal_type
                object["url"] = obj.absolute_url()
                author_id = obj.Creator()
                author = mt.getMemberById(author_id)
                if author:
                    object["author"] = author.getProperty("fullname")
                else:
                    object["author"] = author_id
                object["created"] = context.toLocalizedTime(obj.created())
                object["edited"] = context.toLocalizedTime(obj.modification_date)
                object["icon"] = obj.getIcon()

                if isProductAvailable("ityou.thumbnails"):
                    from ityou.thumbnails.thumbnail import ThumbnailManager
                    object["thumbnail_url"] = ThumbnailManager().getThumbnail(obj)
                else:
                    object["thumbnail_url"] = ""
                objects.append(object)
            else:
                DB.removeObject(user_id, uid)
            
        return objects


    def _copyOrMoveObject(self, move = False, copy = False):
        """ Copy object with given uid to current folder
        Returns UID of new Object or False
        """
        context =   aq_inner(self.context)
        request =   context.REQUEST
        rt =        getToolByName(self, 'reference_catalog')
        catalog =   getToolByName(context, 'portal_catalog')
        ut      =   Utils()

        uid = request.get("uid")
        if not uid:
            logging.warning('Got no UID form the request!')
            return False

        obj =  uuidToObject(uid)
        try:
            obj = obj.aq_inner #LM 2014-08 - problem bei bildern mit der akquisition
        except:
            pass

        creation_date = obj.created()
        
        if move:
            try:
                api.content.move(obj, context)
            except:
                logging.warning('Could not move object!')
                return False
        elif copy:
            try:
                api.content.copy(obj, context)
            except:
                logging.warning('Could not move object!')
                return False
        else:
            return False
        
        folder_path = '/'.join(context.getPhysicalPath())
        brains = catalog(path={'query': folder_path, 'depth': 1}, created=creation_date, sort_on='modified')
        
        new_uid = uid
        if copy:
            i = 1
            while new_uid == uid:
                new_obj = brains[-i].getObject()
                new_uid = new_obj.UID()
                i += 1

        #LM return new_uid
        obj = api.content.get(UID=new_uid)
        return { 'uid': new_uid, 'url': obj.absolute_url(), 'gogo': 'gogo' }


    def _moveObjectToTrash(self):
        """ Move object with given uid to trash folder
        """
        context =   aq_inner(self.context)
        request =   context.REQUEST
        mt =        getToolByName(context, 'portal_membership')
        rt =        getToolByName(self, 'reference_catalog')
        ut =        Utils()

        auth_member = mt.getAuthenticatedMember()
        home_folder = auth_member.getHomeFolder()

        uid = request.get("uid")
        if not uid:
            logging.warning('Got no UID form the request!')
            return False

        ##LM 2014-08 bauch man das???  -------------------------------------
        # Homefolder gehört dem Benutzer immer, oder?
        #if not self.canCopyOrMove(move=True, container=home_folder):
        #    return False

        if not home_folder:
            return False

        # Important: Plone User folder must be activated
        trash_folder = ut.personal_trash_folder(context)
        if not trash_folder:
            return False

        #LM obj = rt.lookupObject(uid)
        obj =  uuidToObject(uid)
        try:
            obj = obj.aq_inner #LM 2014-08 - problem beu bildern mit der akquisition
        except:
            pass
        api.content.move(obj, trash_folder)
        return obj.UID()


    
# --------------------------------------------------------------------------

class AjaxDragDropPermissionsView(BrowserView):
    """Ajax View which handles DragDrop events
    """

    def __call__(self):
        """ Checks the action given in the request and calls the 
        resulting function
        Returns JSON
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        mt      = getToolByName(context, "portal_membership")
        ut      = Utils()
       
        action = request.get('action')
        uid    = request.get('uid')

        if mt.isAnonymousUser():
            return False

        #DEBUG
        print "\n\n__________PERMISSIONS_____________"
        print "ACTION: ", action
        print "UID:    ", uid
       
        if not action:
            res = None
        elif action == 'can_copy':
            res = self._canCopy(context, uid)
        elif action == 'can_move':
            res = self._canMove(context, uid)
        elif action == 'can_delete':
            res = self._canDelete(context)
        else:
            res = False

        return ut.jsonResponse(context, res)


    def _canDelete(self, destination):
        """Check if user can delete objects in the destination folder
        """
        context = aq_inner(self.context)
        sm = getSecurityManager()
        ut = Utils()

        if not ut.personal_trash_folder(context):
            return False

        if not sm.checkPermission(DeleteObjects, destination):   
            return False

        return True


    def _canMove(self, destination, uid):
        """Check if user can move an object form a source folder
        to a destinaction folder
        uid must be given
        """
        sm = getSecurityManager()

        # check if can delete from source folder?
        obj = api.content.get(UID=uid)
        if not obj:
            return False

        source = obj.aq_parent
        if not sm.checkPermission(DeleteObjects, source):   
            return False

        # check if can copy into destination folder
        if self._canCopy(destination, uid=uid):
            return True
        else:
            return False        


    def _canCopy(self, destination, uid=None):
        """Check if user can copy a object into a destinaction folder)
        """
        sm = getSecurityManager()

        # check if can paster into destination folder
        if sm.checkPermission(AddPortalContent, destination):
            if uid:
                # check if there is a content type restriction at destination
                obj = api.content.get(UID=uid)
                allowed_types = destination.getLocallyAllowedTypes()
                if obj.portal_type in allowed_types:
                    return True
            else:
                return True
        return False

# --------------------------------------------------------------------------------------------------------

class Utils():
    """Utilities 
    """

    def personal_trash_folder(self, context):
        """returns trash folder object in the home folder of the user
        If it doesn't exist - create one
        """
        ####context     = aq_inner(self.context)
        mt = getToolByName(context, 'portal_membership')

        if not mt.getAuthenticatedMember():
            return False

        home_folder = mt.getAuthenticatedMember().getHomeFolder()
        if not home_folder:
            return False

        try:
            trash_folder= home_folder[TRASH_FOLDER]
        except KeyError:
            try:
                trash_folder = api.content.create(container= home_folder, type="Folder", id=TRASH_FOLDER, title=context.translate("Trash"))
                trash_folder.setLayout("thumbnail_listing")
            except:
                return False
        return trash_folder        

        
    def jsonResponse(self, context, data):
        """ Returns Json Data in Callback function
        """
        request =  context.REQUEST
        callback = request.get('callback','')        
        request.response.setHeader("Content-type","application/json")
        if callback:
            cb = callback + "(%s);"
            return cb % json.dumps(data)
        else:
            return json.dumps(data)


    
