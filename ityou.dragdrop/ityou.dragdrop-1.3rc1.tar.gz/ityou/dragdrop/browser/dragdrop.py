# -*- coding: utf-8 -*-
## -----------------------------------------------------------------
## Copyright (C)2013 ITYOU - www.ityou.de - support@ityou.de
## -----------------------------------------------------------------
"""
This module contains all views of ityou.dragdrop
"""
from Acquisition import aq_inner

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
import json
from exceptions import KeyError

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
        if mt.isAnonymousUser():
            return False
        
        if not action:
            res = None
        elif action == 'add_object':
            res = self.addObject()
        elif action == 'remove_object':
            res = self.removeObject()
        elif action == 'get_objects':
            res = self.getObjects()
        elif action == 'copy_object':
            res = self.copyOrMoveObject(copy = True)
        elif action == 'move_object':
            res = self.copyOrMoveObject(move = True)
        elif action == 'move_to_trash':
            res = self.moveObjectToTrash()
        elif action == 'can_copy':
            res = self.canCopyOrMove()
        elif action == 'can_move':
            res = self.canCopyOrMove(move = True)
        elif action == 'can_delete':
            res = self.canCopyOrMove(delete = True)
        else:
            res = False
        
        return self.jsonResponse(context, res)

    
    def addObject(self):
        """ Checks the authenticated user id.
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
        return self.jsonResponse(context, DB.addObject(user_id, uid))


    def removeObject(self):
        """ Checks the authenticated user id.
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
        return DB.removeObject(user_id, uid)

    def getObjects(self):
        """ Get objects for the current user
        Returns: 
        [
            {
                uid,
                id,
                title,
                url,
                portal_type,
                thumbnail_url,
            }
            ,
            ...
        ]
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
                object["author"] = author.getProperty("fullname") or author_id
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


    def copyOrMoveObject(self, move = False, copy = False):
        """ Copy object with given uid to current folder
        Returns UID of new Object or False
        """
        context =   aq_inner(self.context)
        request =   context.REQUEST
        rt =        getToolByName(self, 'reference_catalog')
        catalog =   getToolByName(context, 'portal_catalog')

        uid = request.get("uid")
        obj = rt.lookupObject(uid)
        creation_date = obj.created()

        if move:
            api.content.move(obj, context)
        elif copy:
            api.content.copy(obj, context)
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

        return new_uid


    def moveObjectToTrash(self):
        """ Move object with given uid to trash folder
        """
        context =   aq_inner(self.context)
        request =   context.REQUEST
        mt =        getToolByName(context, 'portal_membership')
        rt =        getToolByName(self, 'reference_catalog')

        uid = request.get("uid")
        auth_member = mt.getAuthenticatedMember()
        home_folder = auth_member.getHomeFolder()

        if not self.canCopyOrMove(move=True, container=home_folder):
            return False
        if not home_folder:
            return False

        trash_folder = self._personal_trash_folder()
        if not trash_folder:
            return False

        obj = rt.lookupObject(uid)
        api.content.move(obj, trash_folder)
        return obj.UID()

    
    def canCopyOrMove(self, move = False, container = False, delete = False, context = None):
        """ Checks if current user is allowed to copy file with given uid into current folder
        Returns True / False
        """
        context = context or aq_inner(self.context)
        request = context.REQUEST
        mt =      getToolByName(context, 'portal_membership')
        sm =      getSecurityManager()
        rt =      getToolByName(self, 'reference_catalog')

        if delete:
            container   = self._personal_trash_folder()
        elif not container:
            container = context

        if sm.checkPermission(AddPortalContent, container):
            if move or delete:
                uid = request.get("uid")
                obj = rt.lookupObject(uid)
                if not obj:
                    parent = context
                else:
                    parent = obj.aq_parent
                if not sm.checkPermission(DeleteObjects, parent):
                    return False
            return True
        else:
            return False


    def _personal_trash_folder(self):
        """returns trash folder object in the home folder of the user
        If it doesn't exist - create one
        """
        context     = aq_inner(self.context)

        mt          = getToolByName(context, 'portal_membership')
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

