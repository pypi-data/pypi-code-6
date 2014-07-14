from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from zettwerk.mailtemplates import mailtemplatesMessageFactory as _


class ITemplate(Interface):
    """Description of the Example Type"""

    # -*- schema definition goes here -*-
    templateId = schema.TextLine(
        title=_(u"Template id"),
        required=True,
        description=_(u"a unique id for the template"),
    )
#
