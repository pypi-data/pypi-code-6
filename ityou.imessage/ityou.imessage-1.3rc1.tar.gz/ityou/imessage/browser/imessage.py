# -*- coding: utf-8 -*-
import logging
from time import time
import json
import hashlib
import re
from datetime import datetime, date, timedelta

from Acquisition import aq_inner

from zope.component.hooks import getSite
from zope.interface import implements
from zope.component import getUtility
from zope.component import getMultiAdapter

from plone import api

from plone.memoize.instance import memoize
from plone.registry.interfaces import IRegistry
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from ..dbapi import DBApi
from ..config import TIME_STRING
from ..config import MIN_IMESSAGE_DELAY
from ..interfaces import IInstantMessageSettings
from .. import isProductAvailable
from .. import getNotifyDBApi

from plone.outputfilters.browser.resolveuid import uuidToObject, uuidFor

from stripogram import html2text
try:
    from BeautifulSoup import BeautifulSoup as bs
except:
    from bs4 import BeautifulSoup as bs

from plone import api
from zope.i18n import translate

try:
    from ityou.whoisonline.dbapi import RDBApi as WhoRDBApi
    who_rdb = WhoRDBApi()
except:
    who_rdb = False

# extended user profile
from ityou.extuserprofile.dbapi import DBApi as DBApi_extuserprofile
db_extuserprofile = DBApi_extuserprofile()

# imessage dbapi
db = DBApi()  

# notification via email
from ityou.notify.dbapi import DBApi as NotifyDBApi
from ityou.notify.interfaces import INotifySettings


# ------ redis ---------------------------------------
from ityou.esi.theme.dbapi import RDBApi
rdb = RDBApi()
# ------ /redis --------------------------------------

from ..config import IMESSAGE_REGEX

class InstantMessageView(BrowserView):
    """View of an Instant Message
    """

    html_template = ViewPageTemplateFile('templates/imessage.pt')

    def __call__(self):
        self.request.set('disable_border', True)        
        self.mu = MessageUtils()
        
        self.portal = getSite()
        self.portal_url = getSite().absolute_url()

        ru =  getUtility(IRegistry)
        # *1000: transform milliseconds to seconds
        # We put this value in the Portlet DOM so that
        # jquery can fetch it
        # if value lower than MIN_IMESSAGE_DELAY,
        # we take MIN_IMESSAGE_DELAY
        self.IMESSAGE_DELAY = max([ru.forInterface(IInstantMessageSettings).imessage_delay*1000, MIN_IMESSAGE_DELAY])
        self.ESI_ROOT = self.portal_url
        
        return self.html_template()

    def get_senders_latest_message(self):
        """ Returns the latest message of all senders
        slm: senders_latest_message
        """
        t1 = time()
        slm = []
        
        context = aq_inner(self.context)
        mt      = getToolByName(context,'portal_membership')
        user_id = mt.getAuthenticatedMember().getId()
        
        if user_id:
            slm = db.getLatestMessageOfAllSenders(receiver_id=user_id)
            slm = self.mu.convertMessagesForTemplate(context, slm)
            print "\t\tDAUER get_senders_latest_message (ms):", (time()-t1) * 1000
            return slm
        else:
            return None
        
    def get_dialog(self,max=1000):
        """ Returns the latest message of a given sender
        slms: sender_latest_messages
        """
        t1 = time()
        slms = []
        
        context = aq_inner(self.context)
        sender_id = context.REQUEST.get('sid',False)
        
        mt      = getToolByName(context,'portal_membership')
        user_id = mt.getAuthenticatedMember().getId()
        
        if sender_id and user_id:
            slms = db.getDialog(receiver_id=user_id, 
                                 sender_id=sender_id, 
                                 order_field='timestamp',
                                 reverse_order=True, 
                                 max=max,offset=0, auth_user_id = user_id)              
            slms = self.mu.convertMessagesForTemplate(context, slms)
            print "\t\tDAUER get_dialog (ms):", (time()-t1) * 1000
            return slms
        else:
            return None

    def use_groups(self):
        """check if the auth user can create group chats
        """
        context =     aq_inner(self.context)       
        mt      =     getToolByName(context,'portal_membership')
        auth_user =   mt.getAuthenticatedMember()
        site_admins = api.user.get_users(groupname='Site Administrators')
        if auth_user in site_admins:
            return 1
        else:
            return 0
    
    def sender_data(self):
        """ gets sender data
        """
        context = aq_inner(self.context)
        mt = getToolByName(context, "portal_membership")
        sid = context.REQUEST.get('sid', None)
        member = mt.getMemberById(sid)
        if not member:
            return False
        else:
            return {
                    "id"        : sid,
                    "name"      : member.getProperty("fullname"),
                    "portrait"  : member.getPersonalPortrait(sid, size="pico").absolute_url()
                    } 

     
class AjaxInstantMessageView(BrowserView):
    """Ajax View of an Instant Message
    """

    def __call__(self):
        
        self.mu = MessageUtils()
        self.is_ityou_esi_theme_available = isProductAvailable("ityou.esi.theme")
        
        context = aq_inner(self.context)
        request = context.REQUEST
        
        action = request.get('action')
                        
        if action == 'post_message':
            return self.add_message()
            
        elif action == 'get_messages':
            return self.get_messages()
            
        elif action == 'get_dialog':
            return self.get_dialog()

        elif action == 'message_read_by_receiver':
            return self.set_message_state("approved")
        
        elif action == 'message_hidden_by_receiver':
            return self.set_message_state("hide_receiver")

        elif action == 'message_hidden_by_sender':
            return self.set_message_state("hide_sender")

        elif action == 'message_delete':
            return self.set_message_state("deleted")

        else:
            pass    

    def get_dialog(self):
        """ Returns the dialog between to users 
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        mt      = getToolByName(context,"portal_membership")

        t1 = time()

        timestamp     = request.get('timestamp')
        sender_id     = request.get('sender_id')
        max           = int(request.get('max',"10"))
        offset        = int(request.get('offset',"0"))
        approved      = request.get('approved',False)      
        user_id = mt.getAuthenticatedMember().getId()
        messages= db.getDialog(receiver_id=user_id, 
                               sender_id=sender_id, 
                               timestamp=timestamp,
                               order_field="id",
                               reverse_order=True,  
                               max=max,offset=offset,
                               approved=approved,
                               auth_user_id = user_id)
        messages = self.mu.convertMessagesForTemplate(context, messages)

        #LM@MR: TEST
        #return mu.jsonResponse(context, messages[:-1]) # -1 because the latest message should not be returnd       
        print "\t\tDAUER get_dialog [AJAX] (ms):", (time()-t1) * 1000  
        return self.mu.jsonResponse(context, messages)

    def set_message_state(self, state):
        """The message will be set to delete or read
        """
        context = aq_inner(self.context)
        request = context.REQUEST

        t1 = time()        
        mt      = getToolByName(context,"portal_membership")
        mids     = json.loads(request.get('mids'))
        
        user_id = mt.getAuthenticatedMember().getId()
        try:
            db.setMessageState(receiver_id=user_id, mids=mids,state=state)
        except:
            logging.error('Could not set message state! %s' % state)
        print "\t\tDAUER set_message_state (ms):", (time()-t1) * 1000
        return None


    def get_messages(self):
        """ Returns a list of message from the Database
        #LM vorher: DAUER get_messagee (ms): 364.3883776620
        #LM nachher: DAUER get_messagee (ms): 12.6121044159
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        mt      = getToolByName(context,"portal_membership")
        t1 = time()

        timestamp       = request.get('timestamp', None)

        if timestamp:
            #timestamp       = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            timestamp       = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ") #TODO #LM
        
        sender_id       = request.get('sender_id', False)
        receiver_id     = request.get('receiver_id', False)
        newer           = request.get('newer',False)
        approved        = request.get('approved',False)
        omit_sender     = request.get('omit_sender',False)    
        max             = int(request.get('max',"5"))
        offset          = int(request.get('offset',"0"))
        dialog          = request.get('dialog', False)
        reverse_order   = request.get('reverse_order', True)
        
        user_id = mt.getAuthenticatedMember().getId()

        tx = time()        
        if not receiver_id:
            receiver_ids = self._getReceiverIdsForUser(user_id)
        else: 
            receiver_ids = [receiver_id,]

        if self.is_ityou_esi_theme_available and not receiver_id:
            rdb.delStatus("imessage", uid = user_id)

        messages = db.getMessages(receiver_ids=receiver_ids, 
                                 sender_id=sender_id, 
                                 timestamp=timestamp, 
                                 newer=newer,
                                 order_field='timestamp',
                                 reverse_order= reverse_order, 
                                 max=max,offset=offset,
                                 approved=approved, 
                                 auth_user_id = user_id,
                                 omit_sender = omit_sender, 
                                 dialog = dialog)

        messages = self.mu.convertMessagesForTemplate(context, messages)

        print "\t\tDAUER get_messages (ms):", (time()-t1) * 1000
        return self.mu.jsonResponse(context, messages)


        
    def add_message(self):
        """ Add a message to the Database
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        mt      = getToolByName(context,"portal_membership")

        t1 = time()

        receiver_id         = request.get('receiver_id', False)
        receiver_group_id   = request.get('receiver_group_id', False)
        receiver_group_hash = request.get('receiver_group_hash', False)
        message_text        = request.get('message')
        new_group           = request.get('new_group', False)
        
        # Zum hinzufügen von Nachrichten muss mindestens ein Text + ein Empfänger (Benutzer, Gruppe oder iMessage Gruppe) angegeben sein
        if not ((receiver_id or receiver_group_id or receiver_group_hash) and message_text):
            return None

        # Empfänger als Liste
        if receiver_id:
            receiver_ids = receiver_id.replace(" ","").split(',')
        else:
            receiver_ids = []
        
        # Plone Gruppen als Liste
        if receiver_group_id:
            receiver_group_ids = receiver_group_id.replace(" ","").split(',')
        else:
            receiver_group_ids = []

        # Überorüfung ob Benutzer existieren
        for receiver_id in receiver_ids:
            if receiver_id not in context.acl_users.getUserNames():
                return None
        
        # Überprüfung ob Gruppen existieren
        for receiver_group_id in receiver_group_ids:
            try:
                api.group.get(groupname = receiver_group_id)
            except:
                return None
            
        # Utils initalisieren
        #######mu = MessageUtils()
        
        # Benutzerdaten
        user            = mt.getAuthenticatedMember()
        user_id         = user.getId()
        user_name       = user.getProperty('fullname','').decode('utf-8')
        user_email      = user.getProperty('email', '').decode('utf-8')
        user_portrait   = self.mu.getPersonalPortrait(user_id, size='pico')

        # Wenn iMessage-Gruppe erstellt werden soll,
        # dann Empfänger (Plone-Gruppen und Plone-Benutzer) zu
        # einer Liste vereinen
        if new_group and not receiver_group_hash:
            receiver_ids.extend(receiver_group_ids)
            receiver_ids.append(user_id)
            # Gruppe in Datenbank erstellen und hash speichern
            receiver_group_hash = db.createGroup(receiver_ids, new_group)
            
        # Gruppen-Hash als receiver_id
        if receiver_group_hash:
            receiver_ids = [receiver_group_hash,]

        # Liste mit Benutzern, die benachrichtigt werden sollen (statusflags) initialisieren
        sf_ids = []

        for receiver_id in receiver_ids:
            try:
                receiver_email  = mt.getMemberById(receiver_id).getProperty('email', '').decode('utf-8')
            except:
                receiver_email  = ""
            if new_group:
                receiver_id = receiver_group_hash
            else:
                receiver_id     = receiver_id.decode('utf-8')
            
            for r in IMESSAGE_REGEX:
                regex = re.compile(r["search"])
                message_text = regex.sub(r["replace"], message_text)
                        
            message = {  
                'sender_id':      user_id,      
                'sender_name':    user_name,
                'sender_email':   user_email,
                'receiver_id':    receiver_id,
                'receiver_name':   "",
                'receiver_email': receiver_email,
                'message':        message_text.decode('utf-8'),                                
                }

            latest_message = db.getMessage(request.get('hash'))
            
            timeout = datetime.now() - timedelta(seconds=120)
            
            update = False
            
            message['message']  = message_text.replace('[LF]', '\n').replace('\n', '<br />')

            # Bei Gruppen kein updateMessage!
            nu = NotifyUtils()
            if latest_message and not receiver_group_hash:
                if (latest_message['sender_id'] == message['sender_id']) and (latest_message['timestamp'] > timeout):                
                    update = True
                    message_confirm = db.updateMessage(latest_message['md5'],message['message'], message['receiver_id'])
                else:
                    message_confirm = db.addMessage(message)
            else:
                message_confirm = db.addMessage(message)
    
            # nur notify wenn message in db
            if message_confirm:
                nu.notify(message, message_confirm, mt)

            message['hash']             = message_confirm['md5']
            message['sender_portrait']  = user_portrait
            message['timestamp']        = message_confirm['timestamp'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            message['timestr']          = message_confirm['timestamp'].strftime(TIME_STRING)
            message['update']           = update

            # Wenn iMessage-Gruppe, dann Namen der Gruppe aus Datenbank lesen
            if receiver_group_hash:
                message['receiver_name'] = db.getGroupname(receiver_id)
            else:
                # ansonsten Benutzername (Empfänger) oder ID
                try:
                    message['receiver_name'] = mt.getMemberById(receiver_id).getProperty("fullname")
                except:
                    message['receiver_name'] = receiver_id

            # Statusflags setzen
            # =======================================================================
            if self.is_ityou_esi_theme_available:
                ##from ityou.esi.theme.dbapi import DBApi as StatusFlagsApi
                ##sfapi = StatusFlagsApi()

                if receiver_group_hash:
                    sf_ids = db.getReceiversOfGroup(receiver_group_hash)
                elif receiver_id in receiver_group_ids:                    
                    groupmembers = api.user.get_users(groupname=receiver_id)
                    for groupmember in groupmembers:
                        groupmember_id = groupmember.getId()
                        sf_ids.append(groupmember_id)
                else:
                    sf_ids = [receiver_id,]
                for user in sf_ids:
                    if user == user_id:
                        continue
                    #####sfapi.setStatus("imessage", True, uid = user)
                    rdb.setStatus("imessage", 1, uid = user)
                    #print "IMESSAGE", user, 1
            # =======================================================================
                
            # Wenn iMessage-Gruppe, nicht traversieren
            if receiver_group_hash:
                break

        ###mu = MessageUtils()
        print "\t\tDAUER add_message (ms):", (time()-t1) * 1000

        if who_rdb: 
            who_rdb.setOnlineUser(user_id)
            rdb.setStatus("whoisonline", 1,  uid = user_id, omit_uid = True)

        if receiver_ids:
            return self.mu.jsonResponse(context, message)


    def _getReceiverIdsForUser(self, user_id):
        """ Calculates receiver_ids for user (with groups)
        """
        t1 = time()
        receiver_ids = []
        receiver_ids.append(user_id)
        user_groups = api.group.get_groups(username=user_id)
        for group in user_groups:
            receiver_ids.append(group.getId())
        receiver_ids.extend(db.getGroupsOfUser(receiver_ids))
        print "\t\tDAUER _getReceiverIdsForUser (ms):", (time()-t1) * 1000
        return receiver_ids


class NotifyUtils():
    """Notify utilities
    """

    def notify(self, nm, message_confirm, mt):
        """ write notification to notity-Database
        """

        # pruefe ob notify message eingeschaltet ist
        if not getUtility(IRegistry).forInterface(INotifySettings).imessage_notifications_active:
            return False

        #LM In der Reciever-ID kann auch der Hash der Chat-Gruppe stehen
        uid = mt.getMemberById(nm['receiver_id'])
        auth = mt.getAuthenticatedMember().getId()

        dbapi_notify = NotifyDBApi()
        receivers = []
        chat_group_hash = None

        if uid:
            # dann ist es ein user
            is_notify_receiver = db_extuserprofile.getProperty(nm['receiver_id'], "imessage_notifies")
            if is_notify_receiver:
                receivers = [nm['receiver_id']]
        else:            
            # dann ein chat-gruppen hash
            chat_group_hash = nm['receiver_id']

            # alle empfänger finden
            receivers = db.getReceiversOfGroup(chat_group_hash)

        for receiver_id in receivers:

            if auth != str(receiver_id): # keine mails an sicht selbst verschicken
                if db_extuserprofile.getProperty(receiver_id, "imessage_notifies"):
                    receiver = mt.getMemberById(receiver_id)
                    if chat_group_hash:
                        link = "@@messages?rid=" + chat_group_hash
                    else:
                        link = "@@messages?id=" + receiver_id
                                        
                    dbapi_notify.addNotification({
                        "action":           u'imessage',
                        "sender_id":        nm['sender_id'],
                        "sender_name":      nm['sender_name'],
                        "sender_email":     nm['sender_email'],
                        "receiver_id":              receiver_id,
                        "receiver_name":            receiver.getProperty('fullname'),
                        "receiver_email":           receiver.getProperty('email'),
                        "content_uid":              None,
                        "content_path":             link,
                        "content_title":            None,
                        "message":          nm["message"],
                        "timestamp_mod":    message_confirm['timestamp'],
                         }) 

        return True


class MessageUtils():
    """ Small Utils to render Messages
    """

    def __init__(self):
        self.is_extuserprofile_available = isProductAvailable('ityou.extuserprofile')

    def convertMessagesForTemplate(self, context, ms):
        """ Converts the message dict to what the template needs
        #LM vorher: DAUER convertMessagesForTemplate (ms): 4587.637736637
        #LM nachher: DAUER convertMessagesForTemplate (ms): 63.873052597
        #LM Todo: Logik raus - hier geht es nur im die Aufbreitung der Daten für das Template
        """
        t1 = time()
        messages = []
        if not ms:
            return messages

        mt = getToolByName(context,'portal_membership')
        auth_member = mt.getAuthenticatedMember()
        auth_member_id = auth_member.getId()

        for m in ms:
            #if not m: #LM hää?
            #    continue

            sender_id =     m['sender_id']

            sender = mt.getMemberById(m['sender_id'])            
            if not sender:                
                #LM wenn der Sender nicht mehr existriert, muss die Nachricht raus 2014-05-23
                continue
             
            #LM 2014-05-23   
            #try:
            #    sender    =   mt.getMemberById(m['sender_id'])
            #    sender_exists = True
            #except:
            #    sender = False
            #    sender_exists = False
            #    #LM wenn der Sender nicht mehr existriert, muss die Nachricht raus 2014-05-23
            #    continue

            #LM 2014-05-17
            if sender:
                sender_name = sender.getProperty("fullname")
            else:
                sender_name = '' 
            receiver_id =   m['receiver_id']
            
            is_grouped = False
            if context.REQUEST.get('dialog', False):
                for message in messages:
                    if message["sender_id"] == sender_id and message["receiver_id"] == receiver_id \
                        or message["receiver_id"] == sender_id and message["sender_id"] == receiver_id \
                        or message["receiver_id"] == receiver_id and not mt.getMemberById(message["receiver_id"]):
                        if not m['approved'] and m['sender_id'] != auth_member_id:
                            message['unread'] +=1
                        is_grouped = True
                        break
                if is_grouped:
                    continue

            # if group, else receivers is None
            group_receivers =     db.getReceiversOfGroup(receiver_id)

            """ #LM raus
            group = False
            try:
                receiver_name     = mt.getMemberById(m['receiver_id']).getProperty("fullname")
                ##group = False
            except:
                if(len(receivers) > 0):
                    group = True
                receiver_name   = db.getGroupname(receiver_id)
            """
            # ist der Empfänger eine Gruppe oder ein einzelner Benutzer?

            if mt.getMemberById(m['receiver_id']):
                receiver_name = mt.getMemberById(m['receiver_id']).getProperty("fullname")
                group = False
            elif group_receivers: #LM: es kann vorkommen, dass es Gruppen ohne Benutzer gibt
                receiver_name = db.getGroupname(receiver_id)
                group = True
            else: #LM: kommt vor wenn es den receiver nicht mehr gibt, dann raus damit
                continue

            #print "Group / RECEIVER_NAMES / RECEIVERS: ", group, receiver_name, group_receivers

            # den tag() übertragen da mit json sonst nicht serialisierbar
            sender_portrait   = self.getPersonalPortrait(sender_id, size='pico')
            try:
                receiver_portrait = self.getPersonalPortrait(receiver_id, size='pico')
            except:
                receiver_portrait = "defaultUser.png"

            timestr         = m['timestamp'].strftime(TIME_STRING)
            
            #LM raus 'sender_exists':    sender_exists,
            m_tmpl = {
                'sender_id':        sender_id,
                'sender_name':      sender_name,
                'sender_email':     m['sender_email'],
                'sender_portrait':  sender_portrait,
                'receiver_id':      m['receiver_id'],
                'receiver_name':    receiver_name,
                'receiver_email':   m['receiver_email'],
                'receiver_portrait': receiver_portrait,
                'message':          m['message'],
                'timestamp':        m['timestamp'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'timestr':          timestr,
                'hash':             m['md5'],
                'site_url':         getSite().absolute_url(),
                'approved':         m['approved'],
                'deleted':          m['deleted'],
                'group':            group,
                'unread':           0
            }
            if not m_tmpl['approved'] and m_tmpl['sender_id'] != auth_member_id:
                m_tmpl['unread'] += 1
                
            # Prüfen, ob dies eine Gruppe ist
            #### s.o. ### receivers = db.getReceiversOfGroup(receiver_id)
            receiver_list = []
            if group:
                for r in group_receivers:
                    try:
                        user = mt.getMemberById(r)
                        receiver_id = user.getId()
                        receiver_name = user.getProperty("fullname")
                        tx = time()
                        receiver_list.append({"id"  : receiver_id, "name"   : receiver_name, "portrait" : self.getPersonalPortrait(receiver_id, size="icon") })
                    except:
                        group = api.group.get(groupname = r)
                        if group:
                            group_members = group.getGroupMembers()
                            for member in group_members:
                                member_id = member.getId()
                                in_receivers = False
                                for tr in receiver_list:
                                    if tr["id"] == member_id:
                                        in_receivers = True
                                if not in_receivers and not sender_id == member_id:
                                    tx = time()
                                    receiver_list.append({"id"  : member_id, "name"   : member.getProperty("fullname"), "portrait" : self.getPersonalPortrait(member_id, size="icon") })
            m_tmpl['multiple_receivers'] = receiver_list
            messages.append(m_tmpl)

        print "\t\tDAUER convertMessagesForTemplate (ms):", (time()-t1) * 1000
        return messages

    def jsonResponse(self, context, data):
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

##class PersonalPortraits():
##    """Get url off personal portraits
##    """

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
        #LM if obj ist returned:
            DAUER getPersonalPortrait [MESSAGE] (ms): 383.431196213
        #LM if url is returned:
            DAUER: >>>>>>>>>>>>>>  0.030 ms
        """
        t1 = time()
        plone = getSite()
        mt = getToolByName(plone,"portal_membership")

        if self.is_extuserprofile_available:
            return mt.getPersonalPortrait(id, size=size).absolute_url()
        else:
            return mt.getPersonalPortrait(id=id).absolute_url()


class AjaxUserView(BrowserView):
    """Get Plone-User with ajax
        ===> returns json 
    """
    
    def __call__(self):
        """Standard Json view
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        action  = request.get('action')

        if action == "query":
            return self.query()
        else:
            return False

    def query(self):
        """Query Members
        """
        LIMIT     = 10000

        context   = aq_inner(self.context)
        request   = context.REQUEST

        q         = request.get('q','')
        limit     = int(request.get('l',LIMIT))
        mt        = getToolByName(context,'portal_membership')

        if q:
            users = mt.searchForMembers(name=q)
        else:
            users = mt.listMembers()

        ju = MessageUtils()

        return ju.jsonResponse( context,  self._convert_users(users[:limit])   )

    def _convert_users(self, users):
        """Converts Memberdata = Default user profile + extended!
        """
        context  = aq_inner(self.context)        
        user_list = []
        for u in users:
            #ToDo
            uid = u.getId().decode('utf-8')
            eup = db_extuserprofile.getExtendedProfile(uid)       
            user_list.append({
              "id":         u.getId(), 
              "name":       u.getProperty('fullname'),
              "email":      u.getProperty('email'),  
              "portrait":   u.getPersonalPortrait(u.getId(),size='pico'),
              "phone":      eup.phone or '',
              "location":   u.getProperty("location"),
              "position":   eup.position or '',
              "last_login": context.toLocalizedTime(u.getProperty("login_time"),long_format=1),
              "last_login_timestamp": int(u.getProperty("login_time"))
            })
        return user_list


