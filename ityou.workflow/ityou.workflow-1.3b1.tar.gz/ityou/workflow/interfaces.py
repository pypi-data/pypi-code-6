#-*- coding: utf-8 -*-
from z3c.form import interfaces
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface

_ = MessageFactory('ityou.workflow')

class IWorkflowSettings(Interface):
    """Global workflow settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """
    todo_enabled = schema.Bool(
            title=_(u"Enable ToDo list"),
            description=_(u"You can enable here the ToDo list."),
            required=False,
            default=False,
        )
    
class IWorkflow(Interface):
    """Marker interface
    """
