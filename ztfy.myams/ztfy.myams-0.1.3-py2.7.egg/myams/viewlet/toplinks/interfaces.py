#
# Copyright (c) 2012 Thierry Florac <tflorac AT onf.fr>
# All Rights Reserved.
#


# import standard packages

# import Zope3 interfaces
from zope.viewlet.interfaces import IViewlet, IViewletManager

# import local interfaces

# import Zope3 packages
from zope.schema import TextLine, List, Object, Dict

# import local packages

from ztfy.myams import _


class ITopLinksViewletManager(IViewletManager):
    """Top links viewlet manager interface"""


class ITopLinksMenu(IViewlet):
    """Top link menu"""

    css_class = TextLine(title=_("Menu CSS class"),
                         required=False)

    label = TextLine(title=_("Menu label"))

    click_handler = TextLine(title=_("Menu click handler"))

    url = TextLine(title=_("Menu link location"))

    data = Dict(title=_("Menu data attributes"),
                key_type=TextLine(),
                value_type=TextLine())


class ITopLinksViewlet(IViewlet):
    """Top link viewlet"""

    label = TextLine(title=_("Main label"))

    dropdown_label = TextLine(title=_("Dropdown menu label"))

    css_class = TextLine(title=_("Main CSS class"))

    viewlets = List(title=_("Top links menus"),
                    value_type=Object(schema=ITopLinksMenu))
