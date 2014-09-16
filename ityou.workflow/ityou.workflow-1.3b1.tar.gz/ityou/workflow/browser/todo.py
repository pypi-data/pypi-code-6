# -*- coding: utf-8 -*-
import logging
import time
import json
import random
import md5

from datetime import date, timedelta, datetime

from exceptions import AttributeError

from Acquisition import aq_inner

from zope.component import getMultiAdapter, queryMultiAdapter
from zope.i18nmessageid import MessageFactory
from zope.i18n import translate
from zope.annotation.interfaces import IAnnotations

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.Permissions import AccessPreviousVersions
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.WorkflowCore import WorkflowException
try: 
    from Products.CMFPlacefulWorkflow import ManageWorkflowPolicies 
except ImportError: 
    from Products.CMFCore.permissions import ManagePortal as ManageWorkflowPolicies 
    
from plone.memoize.instance import memoize

from .. import isProductAvailable
from .. import _

from . import TRANSLATION


class TodoView(BrowserView):
    """Show ToDO List View
    """    
    def __call__(self):        
        self.request.set('disable_border', True) 
        context = aq_inner(self.context)
        context.REQUEST.set('action', 'todos')
        return self.index()


class TodoTable(BrowserView):
    """Displays the ToDO Table  
    """

    def __call__(self):   
        
        context = aq_inner(self.context)
        request = context.REQUEST
        
        uid       = request.get('uid')
        wf_event  = request.get('wf_event')
        
        if uid and wf_event:
            self._changeWorkflowState(uid, wf_event)        
            
        return self._todo()


    def _todo(self):
        """ 
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        
        mt = getToolByName(self, 'portal_membership')        
        ct = getToolByName(self, 'portal_catalog')
        rt = getToolByName(self, "portal_repository", None)        
        wf = getToolByName(self, "portal_workflow")

        brains = ct( {'review_state':'pending'} )
        data = []
        
        PMF          = MessageFactory('plone')
        PMF_comment  = MessageFactory('cmfeditions')
        PMF_discussion = MessageFactory('plone.app.discussion')

        for brain in brains:

            task = brain.getObject()
            owner_id = task.getOwner().getId()
            
            if owner_id == "admin":
                continue
            
            av_states = self._getMenuItems(task)

            if not av_states:
                continue
       
            state_options = { "options"  : [ {"id": state["id"], "title": translate(PMF(state["title"]), context=request)} for state in av_states  ]  }                

            version_history = self._revision_history(task)
            
            try:
                last_revision = self._convert_time(task.creation_date.millis()/1000)
            except AttributeError:
                epoch = datetime.utcfromtimestamp(0)
                delta = task.creation_date - epoch
                last_revision = self._convert_time(delta.days*86400+delta.seconds+delta.microseconds/1e6)
            comment = ""
            
            review_state = translate(PMF_comment(brain.review_state))
            
            for version in list(version_history):
                last_revision = self._convert_time(version["time"])
                comment = translate(PMF_comment(version["comments"].decode("UTF-8")), context=request)
                comment = translate(PMF(comment), context=request)
                break
            
            owner_fullname = task.getOwner().getProperty("fullname")
            
            owner_portrait   = '<img class="img-clip" src="%s" title="%s"/>' % (mt.getPersonalPortrait(owner_id).absolute_url(), owner_fullname)
                            
            location = {
                "url"  :  brain.getURL(),
                "task" :  task.title_or_id().decode("UTF-8")
            }
            
            task_uid = brain.UID

            priority = 3
            deadline = "-"

            if isProductAvailable("ityou.annotations"):
                from ityou.annotations import ANNOT
                annotations = IAnnotations(task)
                if ANNOT in annotations:
                    if annotations[ANNOT].has_key('level'):
                        priority = annotations[ANNOT]['level']
                    if annotations[ANNOT].has_key('dline'):
                        deadline = annotations[ANNOT]['dline']

            try:
                data.append([
                    owner_portrait,
                    owner_fullname, 
                    location, 
                    comment, 
                    last_revision,
                    [state_options,  translate(PMF(review_state), context=request)], 
                    task_uid
                    ])
            except:
                logging.error("Fehler: %s not found" % location)
            
        todos = {
                 "iTotalRecords" :1,
                 "iTotalDisplayRecords": 1,
                 "aaData": data
                 }

        self.request.response.setHeader("Content-type","application/json")
        return json.dumps(todos)




    def _convert_time(self, dtime):
        """ Konvertiert Zope-DateTime zu Datum in String-Format
        """

        date_today      = date.today()
        date_yesterday  = date_today - timedelta(1)
        date_edited     = date.fromtimestamp(dtime)
        timestamp       = time.localtime(dtime)

        try:
            if date_edited == date_today: 
                res = '<span class="hiddenStructure">%s</span><span>%s, %s</span>' % (dtime, TRANSLATION["Today"], time.strftime("%H:%M", timestamp))
            elif date_edited == date_yesterday:
                res = '<span class="hiddenStructure">%s</span><span>%s, %s</span>' % (dtime, TRANSLATION["Yesterday"],time.strftime("%H:%M", timestamp))
            else:
                res = '<span class="hiddenStructure">%s</span><span>%s</span>' % (dtime, time.strftime("%d.%m.%y, %H:%M", timestamp))
        except:
            res = '<span class="hiddenStructure">%s</span><span>%s</span>' % (dtime, time.strftime("%d.%m.%y, %H:%M", timestamp))                

        return res

    def _revision_history(self,context):
        if not _checkPermission(AccessPreviousVersions, context):
            return []

        rt = getToolByName(context, "portal_repository", None)
        if rt is None or not rt.isVersionable(context):
            return []

        context_url = context.absolute_url()
        history=rt.getHistoryMetadata(context);
        morphVersionDataToHistoryFormathistory=rt.getHistoryMetadata(context);
        portal_diff = getToolByName(context, "portal_diff", None)
        can_diff = portal_diff is not None \
            and len(portal_diff.getDiffForPortalType(context.portal_type)) > 0

        def morphVersionDataToHistoryFormat(vdata, version_id):
            meta = vdata["metadata"]["sys_metadata"]
            userid = meta["principal"]
            info=dict(type='versioning',
                      action=_(u"Edited"),
                      transition_title=_(u"Edited"),
                      actorid=userid,
                      time=meta["timestamp"],
                      comments=meta['comment'],
                      version_id=version_id,
                      preview_url="%s/versions_history_form?version_id=%s#version_preview" %
                                  (context_url, version_id),
                      revert_url="%s/revertversion" % context_url,
                      )
            if can_diff:
                if version_id>0:
                    info["diff_previous_url"]=("%s/@@history?one=%s&two=%s" %
                            (context_url, version_id, version_id-1))
                if not rt.isUpToDate(context, version_id):
                    info["diff_current_url"]=("%s/@@history?one=current&two=%s" %
                                              (context_url, version_id))
            info.update(self.getUserInfo(userid))
            return info

        if not history:
            return history

        version_history = []
        retrieve = history.retrieve
        getId = history.getVersionId
        for i in xrange(history.getLength(countPurged=False)-1, -1, -1):
            version_history.append(
                morphVersionDataToHistoryFormat(retrieve(i, countPurged=False),
                                                getId(i, countPurged=False)))

        return version_history
    
    @memoize
    def getUserInfo(self, userid):
        mt = getToolByName(self.context, 'portal_membership')
        info=mt.getMemberInfo(userid)
        if info is None:
            return dict(actor_home="",
                        actor=dict(fullname=userid))

        if not info.get("fullname", None):
            info["fullname"]=userid

        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()

        return dict(actor=info,
                    actor_home="%s/author/%s" % (self.site_url, userid))
        
    def _getMenuItems(self, context, request=None):
        """Return menu item entries in a TAL-friendly form."""
        results = []

        locking_info = queryMultiAdapter((context, request), name='plone_lock_info')
        if locking_info and locking_info.is_locked_for_current_user():
            return []

        wf_tool = getToolByName(context, 'portal_workflow')
        workflowActions = wf_tool.listActionInfos(object=context)

        for action in workflowActions:
            if action['category'] != 'workflow':
                continue

            cssClass = 'kssIgnore'
            actionUrl = action['url']
            
            if actionUrl == "":
                actionUrl = '%s/content_status_modify?workflow_action=%s' % (context.absolute_url(), action['id'])
                cssClass = ''

            if action['allowed']:
                results.append({ 'title' : action['title'],
                                 'id'    : action['id'],
                                 })

        return results
    
    def _changeWorkflowState(self, uid, wf_event):

        ut = getToolByName(self.context, "portal_url")
        wf = getToolByName(self.context, "portal_workflow")

        portal = ut.getPortalObject()
        
        ct = getToolByName(self, 'portal_catalog')
        brains = ct({'UID': uid})
        
        if brains:
            object = brains[0].getObject()
        else:
            logging.warning("No object for state transition found! %s" % uid)
            return False
        
        try:
            wf.doActionFor(object, wf_event)
            return True
            
        except WorkflowException:
            logging.error("Workflow State could not be changed! %s" % object.getId() )
            return False        
            
