#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

# Written by Alan Viars
import json, sys, datetime, re


def validate_direct_address_list(l, enumeration_type):
    errors = []
    
    #define a max_length dict
    max_values = {'organization' : 150,
                   'email'       : 150
                 }
    
    #Test for max_length errors    
    
    for d in l:

        for k in max_values.keys():
            if d.get(k):
                if max_values[k] < len(d.get(k)):
                    error = "%s : %s max allowable length %s." % (d.get('email'),  max_values[k])
                    errors.append(error)
    
        #check for required information
        if not d.get('email'):
            error = "%s : email is required." % d.get('email')
            errors.append(error)
    
        if type(d.get('public')) != bool :
            error = "%s : public must be true or false." % (d.get('email'))
            errors.append(error)
    
        if not d.get('organization'):
            error = "%s : organization is required." % (d.get('email'))
            errors.append(error)
    
    
    return errors
    
    