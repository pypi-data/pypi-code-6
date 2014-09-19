# -*- coding: utf-8 -*-
import logging
from five import grok
from datetime import datetime

from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from zope.lifecycleevent.interfaces import IObjectModifiedEvent, IObjectCopiedEvent, IObjectCreatedEvent
#from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFEditions.Permissions import AccessPreviousVersions
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IFolderish
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from ityou.astream.interfaces import IAstreamSettings
from .dbapi import DBApi
from . import getNotifyDBApi, isProductAvailable
from .config import NO_MESSAGES_ON_WORKFLOW_CHANGE
db = DBApi()

# ------ redis ---------------------------------------
from ityou.esi.theme.dbapi import RDBApi
rdb = RDBApi()
# ------ /redis --------------------------------------

#TODO
# @grok.subscribe(IATContentType, ObjectInitializedEvent)
# ...


@grok.subscribe(IATContentType, IObjectModifiedEvent)
def ContentModifyEventHandler(context,event):
    """Content Modified
    """
    logging.info( "\nCONTENT MODIFIED EVENT TRIGGERD: %s\n" % str(event))
    
    request     = context.REQUEST
    form        = request.form
    wt          = getToolByName(context, "portal_workflow")

    user        = request.get('AUTHENTICATED_USER')

    # TODO : Admin and private state should not be logged
    chain = wt.getChainFor(context)
    if chain:
        status = wt.getStatusOf(chain[0], context)
        #logging.info( "CHAIN / STATUS:", chain[0], status)    
        if status:
            if status.get('review_state', None) == "private":
                logging.info("\tPRIVATE")    
                return None
            elif status.get('actor', None) == "admin":
                logging.info( "\tADMIN")
                #return None
    
    if not IFolderish.providedBy(context):
        message = request.get('fieldname')
        if not message:
            utils = Utils()
            message = utils.create_or_edit(context)
            
        activity = {
          "user_id":            user.getId(),
          "user_name":          user.getProperty('fullname','').lstrip(' ').decode('utf-8'),
          "user_email":         user.getProperty('email',''),
          "content_uid":        context.UID(),
          "content_title":      context.Title().decode('utf-8'),
          "content_path":       '/'.join(context.getPhysicalPath()).decode('utf-8'),
          "message":            message
        }
        activity_id = db.addActivity(activity)
        notice = request.get('cmfeditions_version_comment')
        
        if notice:
            comment = {
                "activity_id":      activity_id,
                "user_id":          user.getId(),
                "comment":          notice.decode('utf-8'),
                "revision":         context.version_id
                       }
            if getUtility(IRegistry).forInterface(IAstreamSettings).comment_moderation:
                comment["visible"] = True
            else:
                comment["visible"] = False
                
            db.addComment(comment)
        
        notify_dbapi = getNotifyDBApi()
        if notify_dbapi:
            notify_dbapi.addNotification({
                "action":           u'astream',
                "sender_id":        activity['user_id'],
                "sender_name":      activity['user_name'],
                "sender_email":     activity['user_email'],
                "content_uid":      activity["content_uid"],
                "content_path":     activity["content_path"],
                "content_title":    activity["content_title"],
                "message":          activity["message"],
                "timestamp_mod":    datetime.now(),
                 })
        if isProductAvailable("ityou.esi.theme"):
            rdb.setStatus("astream", 1,  uid = activity['user_id'], omit_uid = True)

    return None
   
@grok.subscribe(IATContentType, IActionSucceededEvent)
def ActivityStreamWorkflowLogging(context,event):
    """ Workflow state change
    """
    logging.info( "WORKFLOW EVENT TRIGGERD: %s\n" % str(event))

    request     = context.REQUEST
    form        = request.form
    wt          = getToolByName(context, "portal_workflow")

    user        = request.get('AUTHENTICATED_USER')
    
    if not IFolderish.providedBy(context):

        # TODO : Admin and private state should not be logged
        chain = wt.getChainFor(context)
        if chain:
            status = wt.getStatusOf(chain[0], context)
            #logging.info( "CHAIN / STATUS:", chain[0], status)    
            if status:
                if status.get('review_state', None) == "private":
                    logging.info("\tPRIVATE")    
                    return None
                elif status.get('actor', None) == "admin":
                    logging.info( "\tADMIN")
                    return None

        message = request.get('workflow_action')
        if message in NO_MESSAGES_ON_WORKFLOW_CHANGE:
            return
        
        if not message:
            message = "workflow"
        
        activity = {
          "user_id":            user.getId(),
          "user_name":          user.getProperty('fullname','').lstrip(' ').decode('utf-8'),
          "user_email":         user.getProperty('email',''),
          "content_uid":        context.UID(),
          "content_title":      context.Title().decode('utf-8'),
          "content_path":       '/'.join(context.getPhysicalPath()).decode('utf-8'),
          "message":            message,
        }
        activity_id = db.addActivity(activity)

        if isProductAvailable("ityou.esi.theme"):
            ###from ityou.esi.theme.dbapi import DBApi as StatusFlagsApi
            ###sfapi = StatusFlagsApi()
            ###sfapi.setStatus("astream", True, user_negative = True, uid = activity['user_id'])   
            # ---- sqlite3 -> redis
            rdb.setStatus("astream", 1,  uid = activity['user_id'], omit_uid = True)
        
        notify_dbapi = getNotifyDBApi()
        if notify_dbapi:
            notify_dbapi.addNotification({
                "action":           u'astream',
                "sender_id":        activity['user_id'],
                "sender_name":      activity['user_name'],
                "sender_email":     activity['user_email'],
                "content_uid":      activity["content_uid"],
                "content_path":     activity["content_path"],
                "content_title":    activity["content_title"],
                "message":          activity["message"],
                "timestamp_mod":    datetime.now(),
                 })

        if isProductAvailable("ityou.esi.theme"):
            ####from ityou.esi.theme.dbapi import DBApi as StatusFlagsApi
            ####sfapi = StatusFlagsApi()
            ####sfapi.setStatus("astream", True, user_negative = True, uid = activity['user_id'])
            # ---- sqlite3 -> redis
            rdb.setStatus("astream", 1,  uid = activity['user_id'], omit_uid = True)
                #"content_path":     activity["content_path"].decode("utf-8"),#warum hier decode??
    return None


class Utils():
    def create_or_edit(self,context):
        if not _checkPermission(AccessPreviousVersions, context):
            return "undefined"

        rt = getToolByName(context, "portal_repository", None)
        if rt is None or not rt.isVersionable(context):
            return "undefined"

        context_url = context.absolute_url()
        history=rt.getHistoryMetadata(context)
        if history.getLength(context) == 1:
            return "create"
        else:
            return "edit"

