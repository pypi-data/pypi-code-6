# -*- extra stuff goes here -*-
from template import ITemplate
ITemplate

from mailtemplatetool import IMailTemplateTool
IMailTemplateTool


from zope.interface import Interface


class IMessageTemplateUserFilter(Interface):

    def getTitle():
        """ returns a translated human readable name of the filter """

    def filterdMembers(members):
        """ filter the list of members like you want """


class IMessageTemplateUserObjectFilter(Interface):

    def getTitle():
        """ returns a translated human readable name of the filter """

    def filterdMembers(members):
        """ filter the list of members like you want """

    def objectList():
        """ return a list of objects, which might be choosen as extra
        filter criterium. """
