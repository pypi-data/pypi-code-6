#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

# Written by Alan Viars
import json, sys, datetime, re
from choices import STATES



def validate_identifier_list(l, enumeration_type):
    errors = []
    primary_count  = 0

    for d in l:
    
        #check for required information
        if d.get('code') not in ("", "01", "02", "04","05", "06", "07", "08"):
            error = "%s : code  is not in ['', '01', '02', '04','05', '06', '07', '08']" % d.get('code')
            errors.append(error)
            
        if not d.get('issuer'):
            error = "%s : issuer is required." % (d.get('code'))
            errors.append(error)
        
        if not d.get('identifier'):
                error = "%s : identifier is required." % (d.get('code'))
                errors.append(error)
        
        #if state is provided then it should be valid.
        if d.get('state') and d.get('state') not in STATES:
            primary_count += 1
    
    return errors