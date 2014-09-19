# -*- coding: utf-8 -*-
import logging
from time import time
from datetime import datetime, timedelta, date
import json

try:
    from BeautifulSoup import BeautifulSoup as bs
except ImportError:
    from bs4 import BeautifulSoup as bs

from stripogram import html2text

from Acquisition import aq_inner

from zope.interface import implements
from zope.component import getUtility
from zope.component.hooks import getSite

from plone.memoize.instance import memoize
from plone.app.uuid.utils import uuidToObject, uuidToCatalogBrain
from plone.registry.interfaces import IRegistry

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from ityou.astream.interfaces import IAstreamSettings

from .. import _

try:
    from ityou.whoisonline import RDBApi as WhoRDBApi
    who_rdb = WhoRDBApi()
except:
    who_rdb = False

from .. import isProductAvailable

from ..config import MESSAGE_TEXT_CONTAINER, TIME_STRING, MIN_ASTREAM_DELAY, ICON_TAG
from ..dbapi import DBApi


from ityou.thumbnails.thumbnail import ThumbnailManager
tm = ThumbnailManager()

db = DBApi()

try:
    from ityou.follow.dbapi import DBApi as DBApi_follow
    dbapi_follow = DBApi_follow()
except:
    is_follow_available = False

# ------ redis ---------------------------------------
from ityou.esi.theme.dbapi import RDBApi
rdb = RDBApi()
# ------ /redis --------------------------------------

class ActivitiesView(BrowserView):
    """View of Activities
    """
    
    html_template = ViewPageTemplateFile('templates/activities.pt')
    
    def __call__(self):
        context = aq_inner(self.context)
        self.au = ActivityUtils()
        context.REQUEST.set('action', 'activities')
        self.site = getSite()
        
        ru =  getUtility(IRegistry)
        # *1000: transform milliseconds to seconds
        # We put this value in the Portlet DOM so that
        # jquery can fetch it
        # if value lower than MIN_ASTREAM_DELAY,
        # we take MIN_ASTREAM_DELAY
        self.ASTREAM_DELAY = max([ru.forInterface(IAstreamSettings).astream_delay*1000, MIN_ASTREAM_DELAY])
        self.ESI_ROOT = self.site.absolute_url() 
        
        # TODO -> 1.2
        self.user_astream = False
        self.separate_streams = False
        #################self.thumbnails_installed = isProductAvailable("ityou.thumbnails")

        mt      = getToolByName(context,"portal_membership")    
        user    = mt.getAuthenticatedMember()

        # -> MR
        self.uid = user.getId()
        return self.html_template()


    def get_activities(self,max_activities=10,max_comments=200,au_id=None):
        """ Read activities out of the Database
        returns a dict with follow keys:
          user_id (int)
          user_name
          user_email
          content_uid
          content title
          content path
          message (text)
          comments (???)
          timestamp (DateTime) 
        """    
        context = aq_inner(self.context)

        ##ToDo --- #LM
        ##uid = context.REQUEST.get('uid')

        acts = db.getActivities(context=context, user_id=au_id, max=max_activities)
        ######################################au = ActivityUtils()
        p_acts = self.au._permission_activities(acts)
        activities = self.au.convertActivitiesForTemplate(context, p_acts)
                
        logging.debug("\n====> ACTIVITIES\n\t\t\t%s" % str(activities))
        return activities
    
    def FollowInstalled(self): # Legacy???? #LM
        """ Test if ityou.follow is installed and functions are available
        """
        return isProductAvailable("ityou.follow")
            

class AjaxActivitiesView(BrowserView):
    """View of an Activity Stream loaded by AJAX and JQ
    """
    
    amount = db.countActivities()

    def __call__(self):
        """
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        mt = getToolByName(context, "portal_membership")
        
        action =        request.form.get('action')
        timestamp =     request.form.get('timestamp', None)        
        uid =           request.form.get('uid')
        comment_id =    request.get('comment_id', False)
        content_uid =   request.get('content_uid', False)    

        self.au = ActivityUtils()

        if action == "get_latest_activities":
            return self.get_latest_activities(uid, timestamp, content_uid)
        elif action == "get_more_activities":
            return self.get_more_activities(uid, timestamp, content_uid)
        elif action == "get_latest_comments":
            return self.get_latest_comments(timestamp)
        elif action == "delete_comment":
            return self.delete_comment(comment_id, content_uid)
        elif action == "activate_comment":
            return self.activate_comment(comment_id, content_uid)
        elif action == "deactivate_comment":
            return self.deactivate_comment(comment_id, content_uid)
        else:
            pass
        
        return None 
            

    def get_latest_activities(self, uid, timestamp, content_uid = None):
        """ Read activities out of the Database
        returns a dict with following keys:
          user_id (int)
          user_name
          user_email
          content_uid
          content title
          content path
          message (text)
          comments (???)
          timestamp (DateTime) 
        """
        t1 = time()
            
        context = aq_inner(self.context)
                    
        # ==== search new activities ===================================
        # 1. Check if there are new activities
        #    that are not yet displayed in the browser!
        #    - read Timesstamp of the latest activity
        #      from the request 
        #    - generate select: new timestamp > latest timestamp
        # 2. Send activities back as JSON Obj.
        # --------------------------------------------------------------

        if timestamp:
            acts = db.getActivities(context=context, user_id=uid, timestamp=timestamp, content_uid=content_uid, order_field='timestamp')
        else:
            acts = db.getActivities(context=context, user_id=uid, content_uid=content_uid )

        p_acts = self.au._permission_activities(acts)

        tc = time()
        activities = self.au.convertActivitiesForTemplate(context, p_acts)
        print "\t\tDAUER    get_latest_activities (ms):", (time() - t1)*1000
        return self.au.jsonResponce(context, activities)


    def get_more_activities(self, uid, timestamp=False, content_uid = None):
        """ Read activities out of the Database
        """
        context = aq_inner(self.context)

        if not timestamp or timestamp == "":
            timestamp = datetime.now()

        acts = db.getActivities(context=context, user_id=uid, timestamp=timestamp, content_uid=content_uid, order_field='timestamp', newer=False)
        p_acts = self.au._permission_activities(acts)
        activities = self.au.convertActivitiesForTemplate(context, p_acts)

        return self.au.jsonResponce(context, activities)

        
    def get_latest_comments(self, timestamp):
        """ Read comments out of the Database
        returns a dict with following keys:
          user_id (int)
          user_name
          user_email
          comment
          timestamp (DateTime)
        """
            
        context = aq_inner(self.context)
        cos = db.getComments(timestamp=timestamp, newer=True)
        mt = getToolByName(context, "portal_membership")
        uid = mt.getAuthenticatedMember().getId()
        
        #Lm Performance killer raus #######if isProductAvailable("ityou.esi.theme"):
        ########## rdb.setStatus("astream_comments", '') # Warum wir hier der Flag gesetzt (get_latest...) #LM
       
        comments = self.au.convertCommentsForTemplate(context, cos)
        return self.au.jsonResponce(context, comments)

    def delete_comment(self, comment_id, content_uid):
        """ Deletes comment with comment id if user is author
        """
        context = aq_inner(self.context)
        obj = uuidToObject(content_uid)
        mt = getToolByName(context, "portal_membership")
        
        if obj.Creator() == mt.getAuthenticatedMember().getId():
            #return db.deleteComment(comment_id, content_uid)
            return self.au.jsonResponce(context, db.deleteComment(comment_id, content_uid) )
        else:
            return False
    
    def activate_comment(self, comment_id, content_uid):
        """ Activates comment with comment id if user is author
        """
        context = aq_inner(self.context)    
        obj = uuidToObject(content_uid)
        mt = getToolByName(context, "portal_membership")
        
        rdb.setStatus("astream_comments", 1)
        if obj.Creator() == mt.getAuthenticatedMember().getId():
            #return db.activateComment(comment_id, content_uid)
            return self.au.jsonResponce(context, db.activateComment(comment_id, content_uid) )
        else:
            return False

    def deactivate_comment(self, comment_id, content_uid):
        """ DEActivates comment with comment id if user is author
        """
        context = aq_inner(self.context)    
        obj = uuidToObject(content_uid)
        mt = getToolByName(context, "portal_membership")
        
        if obj.Creator() == mt.getAuthenticatedMember().getId():
            return self.au.jsonResponce(context, db.deactivateComment(comment_id, content_uid) )
        else:
            return False

class AjaxPostCommentView(BrowserView):
    """View for the comment posts
    Returns an activity_comment dict as json
    """

    def __call__(self):
        
        context = aq_inner(self.context)
        request = context.REQUEST
        mt      = getToolByName(context,"portal_membership")
        
        user      = mt.getAuthenticatedMember()
        user_id   = user.getId()
        user_name = user.getProperty('fullname').decode('utf-8')

        au = ActivityUtils()                
        ####LM portrait  = au.getPersonalPortrait(user_id, size='pico').absolute_url()
        ## FB
        portrait = ""
        ##
        au.getPersonalPortrait(user_id, size='pico')
        content_uid = request.get('id')
        obj = uuidToObject(content_uid)

        try:
            version_id = obj.version_id
        except:
            version_id = 0

        comment_txt = request.get("comment").replace("\n","[LF]")         
        comment = {
                'activity_id':  content_uid,
                'user_id':      user_id,      
                'user_name':    user_name,
                'user_email':   user.getProperty('email').decode('utf-8'),
                'portrait':     portrait,
                'comment':      html2text(comment_txt).replace("[LF]","\n").decode('utf-8'),
                'site_url':     getSite().absolute_url(),
                'revision':     version_id
            }

        if getUtility(IRegistry).forInterface(IAstreamSettings).comment_moderation:
            comment["visible"] = False
        else:
            comment["visible"] = True

        latest_comment = db.getLatestActivityComment(comment['activity_id'])        
        timeout = datetime.now() - timedelta(seconds=30) # 30 Sekunden werden die Comments zusammen gefasst

        if who_rdb: 
            # track online user
            who_rdb.setOnlineUser(user_id)
            # set ststus flag
            rdb.setStatus("whoisonline", 1,  uid = user_id, omit_uid = True)
        
        try:            
            if (latest_comment['user_id'] == comment['user_id']) and (latest_comment['timestamp'] > timeout):                
                comment_confirm = db.updateComment(latest_comment['id'],comment)
            else:
                comment_confirm = db.addComment(comment)
        except:
            comment_confirm = db.addComment(comment)
                            
        timestamp = datetime.strptime(comment_confirm['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        
        comment['timestamp'] = comment_confirm['timestamp']
        comment['timestr']   = timestamp.strftime(TIME_STRING)
        comment['comment']   = comment_txt.replace('[LF]','\n')
        comment['id'] = comment_confirm["id"]

        # set status flag
        rdb.setStatus("astream_comments", 1)

        return au.jsonResponce(context, comment)


class AstreamPostActivity(BrowserView):
    """ Called by Javascript when sending an activity
    """

    def __call__(self):
        #if not getUtility(IRegistry).forInterface(IAstreamSettings).allow_user_activities:
        return False
        context = aq_inner(self.context)
        request = context.REQUEST
        mt = getToolByName(context, "portal_membership")
        auth_member = mt.getAuthenticatedMember()
        
        a = {
            "user_id"         : auth_member.getId().decode("utf-8"),
            "user_name"       : auth_member.getProperty("fullname").lstrip(" ").decode("utf-8"),
            "user_email"      : auth_member.getProperty("email").decode("utf-8"),
            "content_uid"     : u"",
            "content_title"   : u"",
            "content_path"    : u"",
            "message"         : request.get("a").decode("utf-8"),
            'site_url':         getSite().absolute_url()
             }
        
        try:
            db.addActivity(a)
            return True
        except:
            return False      


class ActivityUtils():
    """small utils
    """

    def __init__(self):
        """Initialising variables
        """
        self.is_extuserprofile_available = isProductAvailable('ityou.extuserprofile')
        self.is_follow_available = isProductAvailable("ityou.follow")
        self.is_thumbnail_available = isProductAvailable("ityou.thumbnails")

    def _permission_content(self,acts):
        """ Returns only content to the user that he/she
        is allowed to see
        """        
        return [ uuidToObject(a['id']) for a in acts ]
    
    def _permission_activities(self, acts):
        """ Display only activities which are linked to
        documents the the user is allowed to see
        """
        return [ a for a in acts if uuidToCatalogBrain(a['id']) or a['id'] == ""  ]
    

    def convertActivitiesForTemplate(self, context, acts):
        """Prepares activities to be displayed in the Template
        """        
        mt = getToolByName(context,'portal_membership')
        auth_member_id = mt.getAuthenticatedMember().getId()
                
        activities = []
        tx = time()
        ###LM ???? au = ActivityUtils()

        for a in acts:
            user_id  = a['user_id']                 
            content  = uuidToObject(a['id'])

            if not content and a['id'] != "":
                continue
            
            user = mt.getMemberById(user_id)
            # es kann vorkommen dass der User gelöscht wurde #LM 2014-05-23
            if not user:
                logging.warn('Activity: user %s no longer exists!' % user_id)
                continue

            elif content:
                portal_type = content.portal_type
                content_url = content.absolute_url()
                content_creator = content.Creator()
                allow_comments = getattr(content, 'allow_discussion', False) ## True #DEBUFG content.allow_discussion 
                tag = '<i class="contenttype-%s">' % portal_type.lower()

                #LM 2014-05-13
                icon = content.getIcon()
                if icon:
                    icon_tag = ICON_TAG % (icon)
                else:
                    icon_tag = ""


                if a['content_title']:
                    content_title  = a['content_title']

                    if MESSAGE_TEXT_CONTAINER.has_key(a['message']):
                        message = _(MESSAGE_TEXT_CONTAINER[a['message']], mapping = {"name": content_title, "tag": tag, "icon": icon_tag})
                    else:
                        message = _(MESSAGE_TEXT_CONTAINER.get('undefined'), mapping = {"name": content_title, "tag": tag, "icon": icon_tag})
                else:
                    content_title  = content.title_or_id()
                    message = _(MESSAGE_TEXT_CONTAINER.get('create'), mapping = {"name": content_title, "tag": tag, "icon": icon_tag})            
            else:
                content_uid = None
                content_title = None
                content_url = None
                content_creator = None
                allow_comments = None
                message = a['message']

            # Translation: use ___context____!!!: context.translate
            message = context.translate(message)
            portrait = self.getPersonalPortrait(user_id, size="pico")
            timestr = a['timestamp'].strftime(TIME_STRING)
            
            # Adding followers param
            following = self._is_following(auth_member_id, user_id)
            """
            if self.is_follow_available:
                if dbapi_follow.isFollowing(auth_member_id, user_id):
                    following = "following"
                else:
                    following = "not-following"
            else:
                following = "no-ityou-follow" 
            """
            ##### #LM siehe oben #### user = mt.getMemberById(user_id)
                      
            a_tmpl = {
              "user_id":        user_id, 
              "portrait":       portrait,              
              "user_name":      user.getProperty("fullname", user_id),
              "user_email":     user.getProperty("email", ""),  
              "content_title":  content_title,
              "content_url":    content_url,
              "content_creator": content_creator,
              "id":             a['id'],
              "message":        message,
              "timestr":        timestr,
              "timestamp":      a['timestamp'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
              'site_url':       getSite().absolute_url(),
              'portal_type':    portal_type,
              'follow_available': self.is_follow_available,
              'following':      following,
              'allow_comments': allow_comments,
            }
            if hasattr(content, 'version_id'):
                a_tmpl['revision'] = content.version_id
            else:
                a_tmpl['revision'] = None

            a_tmpl["thumbnails_available"] = self.is_thumbnail_available
            if a_tmpl["thumbnails_available"]:
                a_tmpl["thumbnail_url"] = tm.getCachedThumbnail(content) 

            comments = []
            
            for c in a['comments']:   

                # visible, if #LM sollte nicht hier sondern in der Abfrage gemacht werden #ToDo
                # - content Creator == authenticated user
                # - comment is your own comment
                #print "ioioioioioioioioioioioioioioioioioioioioioioioioioioioioioioio"
                #print "c['user_id']", c['user_id'], mt.getAuthenticatedMember().getId()
                #if c["visible"] ==  False \
                #                    and ( content.Creator() != mt.getAuthenticatedMember().getId() ) \
                #                    and ( c['user_id'] != mt.getAuthenticatedMember().getId() ) :
                #    continue
                if not self._display_comment( c['user_id'], content.Creator(), mt.getAuthenticatedMember().getId(), c['visible']  ):
                    continue

                uid =    c['user_id']
                user =   mt.getMemberById(uid)
                # es kann vorkommen dass der User gelöscht wurde
                if not user:
                    logging.warn('Comment: user %s no longer exists!' % uid)
                    continue

                c_tmpl = {
                    'id'  :         c["id"],
                    'user_id':      uid,
                    'user_name':    user.getProperty("fullname", uid),
                    'user_email':   user.getProperty("email", ""),
                    'comment':      c['comment'],
                    'timestamp':    c['timestamp'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    'timestr':      c['timestamp'].strftime(TIME_STRING),    
                    'portrait':     self.getPersonalPortrait(uid, size="icon"), 
                    'site_url':     getSite().absolute_url() ,
                    'revision':     c['revision'],
                    'visible':      c['visible']
                }                
                comments.append(c_tmpl)
            
            a_tmpl['comments'] = comments 
            activities.append(a_tmpl)                

        return activities

    def _is_following(self,auth_member_id, user_id):
        """ returns
        "folloging", "not-following", 'no-ityou-follow'
        """
        # Adding followers param
        if self.is_follow_available:
            if dbapi_follow.isFollowing(auth_member_id, user_id):
                following = "following"
            else:
                following = "not-following"
        else:
            following = "no-ityou-follow" 
        return following


    def convertCommentsForTemplate(self, context, cos):
        """Prepares comments to be rendered in a jquery-Template
        """
        mt       = getToolByName(context,'portal_membership')
        comments = []
        
        content_objects = {}
        
        for c in cos:
            if not content_objects.has_key(c.activity_id):
                content_objects[c.activity_id] = uuidToObject(c.activity_id)

            #if c.visible == False and content_objects[c.activity_id].getOwner().getId() != mt.getAuthenticatedMember().getId():
            #    continue

            coa = content_objects[c.activity_id]
            if coa:
                if not self._display_comment( c.user_id, coa.Creator(), mt.getAuthenticatedMember().getId(), c.visible ):
                    continue

            uid  =    c.user_id
            user =    mt.getMemberById(uid)
            # es kann vorkommen dass der User gelöscht wurde
            if not user:
                logging.warn('Converting Comment: user %s no longer exists!' % uid)
                continue

            c_tmpl = {
                'id':           c.id,
                'user_id':      uid,
                'user_name':    user.getProperty("fullname", uid),
                'user_email':   user.getProperty("email", ""),
                'comment':      c.comment,
                'timestamp':    c.timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),   
                'timestr':      c.timestamp.strftime(TIME_STRING),
                'portrait':     self.getPersonalPortrait(uid, size="icon"),
                'activity_id':  c.activity_id,
                'site_url':     getSite().absolute_url(),
                'revision':     c.revision,
                'visible':      c.visible
            }
            
            comments.append(c_tmpl)
                                    
        return comments

    def _display_comment(self, comment_uid, creator_id, auth_uid, visible):
        """ True, if authenticated user should see the comment,
            else False
        """

        # visible, if #LM sollte nicht hier sondern in der Abfrage gemacht werden #ToDo
        # - content Creator == authenticated user
        # - comment is your own comment
        if visible ==  False \
                            and ( creator_id != auth_uid ) \
                            and ( comment_uid != auth_uid ) :
            return False
        else:
            return True

    def jsonResponce(self, context, data):
        """ Returns Json Data in Callback function
        """
        request = context.REQUEST
        callback = request.get('callback','')        
        request.response.setHeader("Content-type","application/json")
        if callback:
            cb = callback + "(%s);"
            return cb % json.dumps(data)
        else:
            return json.dumps(data)

    @memoize    
    def getSmallPortrait(self,portrait,username,size="small-personal-portrait"):
        """ rermoves width and height attributes
            and adds a class to the img tag
            if jquery is rendering the image, we only need
            the src of the image
        """
        soup = bs(portrait)
        img = soup.img
        return str(img['src'])

    @memoize
    def getPersonalPortrait(self,id=None, verifyPermission=0, size=None):
        """Adapts the original getPersonalPortrait 
        If ityou.extpersonalportrait is installed, the
        patched personal portrai will be called, else the
        default
        Return absolute_url, not Object, need to memoize 
        for better performance
        """
        plone = getSite()
        mt = getToolByName(plone,"portal_membership")

        #if isProductAvailable('ityou.extuserprofile'):
        if self.is_extuserprofile_available:
            res = mt.getPersonalPortrait(id, size=size).absolute_url()
        else:
            res = mt.getPersonalPortrait(id=id).absolute_url()
        return res
    


