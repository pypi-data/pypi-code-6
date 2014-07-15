#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime 
import pytz 

# current time
def utc_now():
  dt = datetime.utcnow()
  return dt.replace(tzinfo=pytz.utc)
