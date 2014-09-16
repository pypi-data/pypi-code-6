#-*- coding: utf-8 -*-
import smtplib
import mimetypes
import logging
import inspect
import operator
import itertools
import datetime

from stripogram import html2text 
from plone import api
from AccessControl.ImplPython import rolesForPermissionOn

from zope.component.hooks import getSite

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Acquisition import aq_inner

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from ityou.notify.interfaces import INotifySettings

# ---- mailer --------
from email import encoders
from email.message import Message
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
# ---- /mailer --------

from .. import ASTREAM, IMESSAGE
##from .. import DB_LOCATION, DB, TABLE
from .. import SUBJECT, BODY
from .. import DEBUG, DEBUG_EMAIL_ADR
from ..dbapi import DBApi

dbapi = DBApi()

class message():
    """All fields needed to send an message  
    """
    #LM ?????

class SendNotifications(BrowserView):
    """ View which is called by timer. Gets the notifications from dbapi,
    prepare it and send them
    """

    def __call__(self):
        """Default view 
        """
        # check if notifications are enabled
        enabled_ns = self._notification_enabled()
        if not (enabled_ns.has_key(ASTREAM) or enabled_ns.has_key(IMESSAGE)):
            # actually we only have the two apps
            return None        

        # retrieve notifications % prepare emails
        mails = []
        if enabled_ns.has_key(ASTREAM):
            qns = dbapi.getQueuedNotifications(ASTREAM)            
            if qns:
                mails.extend( self._createAStreamMails(qns)  )
            
        if enabled_ns.has_key(IMESSAGE):
            qns = dbapi.getQueuedNotifications(IMESSAGE)
            if qns:
                mails.extend( self._createIMessageMails(qns) )
    
        # send all mails        
        logging.info("Sending %s notifications via email" % len(mails))

        for m in mails:
            if self._sendNotification(m):
                if m['action'] == ASTREAM:
                    trigger = ASTREAM
                    for content in m['content']:
                        content_uid =   content['content_uid'] 
                        timestamp_mod = content['timestamp_mod']
                        dbapi.markNotificationAsSent( trigger, timestamp_mod , content_uid = content_uid )
                elif m['action'] == IMESSAGE:
                    trigger = IMESSAGE
                    content_uid =   None                    
                    timestamp_mod = m['timestamp_mod']
                    dbapi.markNotificationAsSent( trigger, timestamp_mod , content_uid = content_uid )
        return len(mails)
    

    def _notification_enabled(self):
        """checks if at least one notification is enabled
           return dict with enabled apps
        """
        np = getUtility(IRegistry).forInterface(INotifySettings)
        
        enable = {}
        if np.astream_notifications_active:
            enable[ASTREAM] = True        
        if np.imessage_notifications_active:
            enable[IMESSAGE] = True
        return enable

    def _createIMessageMails(self,qns):
        """Creates all mails out off the queued messages
        """
        context =   aq_inner(self.context)
        site_url =  getUtility(IRegistry).forInterface(INotifySettings).site_url or getSite().absolute_url()
        mt      =   getToolByName(context,'portal_membership')

        nmails = []        
        for n in qns:
            # BUG #LM funktioniert nur im direkten dialog - nicht mit gruppenchats
            content_url = site_url + '/'  + n.content_path 
            try:
                message = None
                message = html2text(n.message, indent_width=4,page_width=80).replace("[LF]","")                
            except:
                message = None
                m1 = n.message.encode('utf-8','ignore')
                m2 = html2text(m1, indent_width=4,page_width=80).replace("[LF]","")               
                message = m2.decode('utf-8','ignore')
            m = {}
            m['action'] =           n.action
            m["timestamp_mod"] =    n.timestamp_mod
            m['receiver_id'] =      n.receiver_id
            m['receiver_name'] =    n.receiver_name or ''
            m['receiver_email'] =   n.receiver_email
            m['subject'] =          SUBJECT[IMESSAGE] % {'sender_name': n.sender_name}
            m['body'] =             BODY[IMESSAGE]  % {
                                            'content_url': content_url, 
                                            'message': message,
                                            'receiver_name': n.receiver_name,
                                            'sender_name': n.sender_name
                                            }            
            nmails.append(m)            
        return nmails

    def _createAStreamMails(self,qns):
        """Creates all mails out off the queued astream actions      
        """
        context = aq_inner(self.context)
        site_url = getUtility(IRegistry).forInterface(INotifySettings).site_url or getSite().absolute_url()
        mt      = getToolByName(context,'portal_membership')
        catalog = getToolByName(context, "portal_catalog")
        uids    = mt.listMemberIds()

        nmails = []
        for n in qns:
            # Notification triggered by astream
            try:
                doc = catalog.search({"path":n.content_path})[0].getObject()
                for uid in uids:
                    if self._checkPermission(uid, doc, 'View') and uid != n.sender_id:
                        user = mt.getMemberById(uid)
                        content_url = site_url + n.content_path
                        m = {}
                        m['action'] =           n.action
                        m['receiver_id'] =      uid
                        m['receiver_name'] =    user.getProperty("fullname",'').decode('utf-8')
                        m['receiver_email'] =   user.getProperty("email")
                        m['subject'] =          SUBJECT[ASTREAM]
                        m['content'] =          {  'content_url': content_url, 
                                                   'content_title': n.content_title,
                                                   'content_uid':   n.content_uid,
                                                   'timestamp_mod':  n.timestamp_mod   } 
                        nmails.append(m)
            except IndexError:
                logging.error("astream notification with title '%s' could not be send" % n.content_title)
        
        # find grouped receiver_ids
        gmails = []
        rs = []
        for nmail in nmails:
            rs.append(nmail['receiver_id'])   
        rids = list(set(rs))

        # create empty dict with receiver_ids            
        for rid in rids:
            gmails.append({'receiver_id': rid})
        
        # fill grouped mails
        for gm in gmails:
            gm['content'] = [] ###
            for m in nmails:
                if m['receiver_id'] == gm['receiver_id']:
                    gm['action'] =          m['action']
                    gm['receiver_name'] =   m['receiver_name']
                    gm['receiver_email'] =  m['receiver_email']
                    gm['subject'] =         m['subject']
                           
                    gm['content'].append(m['content']) ###
                       
                    if not gm.has_key('body'):
                        gm['body'] = ''
                    gm['body'] += '\t' \
                        + m['content']['content_title']    + '\n\t' \
                        + m['content']['content_url']      + '\n\t' \
                        + datetime.datetime.strftime(  m['content']['timestamp_mod'], '%d.%m.%Y %H:%M'  ) + '\n\n'
            gm['body'] = BODY[ASTREAM] % {'receiver_name': gm['receiver_name'], 'body': gm['body'] }
            
        return gmails
    
                
    def _sendNotification(self, nm):
        """sends one email notification
        nm = notification message =  {
            'action':          
            'receiver_id':
            'receiver_email':
            'body':
            'content_uid',
            'timestamp_mod'
          }
        """
        context =    aq_inner(self.context)
        mail_host =  getToolByName(context, 'MailHost')
        np =         getUtility(IRegistry).forInterface(INotifySettings)          

        # --- email erstellen
        m_header =   np.email_header or u''
        m_footer =   np.email_footer or u''
        m_from =     getSite().getProperty('email_from_address')
        m_to =       nm["receiver_email"]
        m_subject =  nm["subject"]        
        m_body =     m_header + "\n" + nm["body"] + m_footer
        
        # --- mailbody erstellen ----
        msg =        MIMEMultipart()
        text =       MIMEText( m_body.encode('utf-8'), 'plain' , 'utf-8')
        msg.attach(text)
        # --- mailheader erstellen ------
        msg['Subject']  = m_subject.encode('utf-8')
        msg['From']     = m_from
        msg['To']       = m_to
        try:
            #  --- MAIL WIRD VERSCHICKT !!! ---------------
            logging.info(   "\t\t to: %s (%s)" % (nm['receiver_email'], nm['receiver_id'])   )
            s = smtplib.SMTP(mail_host.smtp_host) 
            if not DEBUG:
                s.sendmail(m_from, m_to , msg.as_string())
            else:
                # --- DEBUG --------------------------------------------
                if DEBUG_EMAIL_ADR:
                    logging.debug('Send debug notification email')
                    s.sendmail(m_from, DEBUG_EMAIL_ADR , msg.as_string())
                else:
                    logging.warn('Could not send debug email because debug email adress is missing, aborting')
        except:
            logging.error("EMail to '%s' could not be send" %  msg['To'] )
            return False
        finally:
            s.quit()

        return True


    def _checkPermission(self, user_id, object, permission):
        """ Checks permission for user on content object 
        """
        if api.user.get_permissions(username=user_id, obj=object)[permission]:
            return True
        else:
            roles_of_permission = object.rolesOfPermission(permission)
            for role in api.user.get_roles(username=user_id, obj = object):
                for role_of_permission in roles_of_permission:
                    if role_of_permission["name"] == role \
                        and role_of_permission["selected"] == 'SELECTED':
                        return True
        return False



