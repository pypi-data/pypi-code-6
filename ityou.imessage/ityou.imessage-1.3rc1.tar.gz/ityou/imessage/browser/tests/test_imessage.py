# -*- coding: utf-8 -*-
import logging
from time import time
import json
import hashlib
import re
from datetime import datetime, date, timedelta

from Acquisition import aq_inner

from zope.component.hooks import getSite
from zope.component import getUtility

from plone import api

from plone.registry.interfaces import IRegistry
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


# -------------------------------------
from ityou.imessage.dbapi import DBApi
db = DBApi()  


class TestInstantMessageView(BrowserView):
    """TEST View of an Instant Message
    """


    def __call__(self):
        """ TESTS
        """        
        context = aq_inner(self.context)

        messages = db.getMessagesForDialogOverview(\
                    receiver_ids =  ['lmeise', 'hmustermann'], \
                    sender_id =     'lmuller', \
                    timestamp =     datetime.now(), \
                    newer =         False, \
                    group_field =   'sender_id', \
                    order_field =   "id", \
                    reverse_order = True, \
                    approved =      False, \
                    omit_sender =   False, \
                    max=20, offset = 0, 
                    auth_user_id =  'lmuller')

        context.REQUEST.RESPONSE.setHeader('content-type', 'text')
        return "===============\n" + str(len(messages)) + '\n' + str(messages)
        

    










