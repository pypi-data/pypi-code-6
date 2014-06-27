# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EKE Site: initialization.
'''

from zope.i18nmessageid import MessageFactory

ProjectMessageFactory = MessageFactory('edrnsite.portlets')

def initialize(context):
    '''Initializer called when used as a Zope 2 product.'''
    pass
    
