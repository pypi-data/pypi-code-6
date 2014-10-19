from django import template
from tinycms.models import *

register = template.Library()

"""
@register.tag(name="show_absolute_menu")
def show_absolute_menu(parser, token):
    Page.objects.root_nodes()


class TinycmsMenuAbsolute(template.Node):
    def render(self):
        pass
"""


@register.simple_tag(takes_context=True)
def show_contents(context, value_name,contentTag=None):
    """Show cms content.

    Variables:
    value_name -- value_name of contents to be shown.
    contentTag -- When contentTag is not None, Each content is tagged by contentTag like <contentTag>content</contentTag>
    """
    valList = context[value_name]

    result =""

    for item in valList:
        if(contentTag):
            result += "<%s>%s</%s>" % (contentTag,item,contentTag)
        else:
            result += "%s" % item
    return result


