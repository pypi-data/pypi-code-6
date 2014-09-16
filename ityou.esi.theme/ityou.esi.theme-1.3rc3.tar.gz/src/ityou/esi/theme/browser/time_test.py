# -*- coding: utf-8 -*-
import time
from datetime import datetime
from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class TimeTestView(BrowserView):
    
    def __call__(self):
        """
        """
        context = aq_inner(self.context)
        request = context.REQUEST

        print "Datetime Local Server:", datetime.now()
        print "Datetime UTC Server  :", datetime.utcnow()
        print "OFFSET:",  datetime.utcnow().replace(minute=0, second=0, microsecond=0) - datetime.now().replace(minute=0, second=0, microsecond=0)
        print "Time Server:", time.time()

        print "LOCAL_TIME OFFSET (H):", self.local_time_offset()
        now = datetime.now()

        
        return now.str
    
        ## timestamp: utc to local
        local_offset = datetime.utcnow().replace(minute=0, second=0, microsecond=0) - datetime.now().replace(minute=0, second=0, microsecond=0)

    def local_time_offset(self,t=None):
        """Return offset of local zone from GMT, either at present or at time t."""

        print "DAYLIGHT", time.daylight, type(time.daylight)
        print "time.localtime(t).tm_isdst", time.localtime(t).tm_isdst

        if time.localtime(t).tm_isdst and time.daylight:
            return -time.altzone
        else:
            return -time.timezone

    


