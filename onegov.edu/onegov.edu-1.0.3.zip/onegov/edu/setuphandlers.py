from zope.component import getUtility
from simplelayout.base.configlet.interfaces import ISimplelayoutConfiguration


SL_CONFIGURATION = {
    'same_workflow': False,
    'show_design_tab' : True,
    'small_size': 124,
    'middle_size': 262,
    'full_size': 537,
    'small_size_two': 54,
    'middle_size_two': 118,
    'full_size_two': 265}


def configure_simplelayout(portal):
    sl_conf = getUtility(ISimplelayoutConfiguration, name='sl-config')
    for key in SL_CONFIGURATION:
        setattr(sl_conf, key, SL_CONFIGURATION[key])


def import_various(context):
    """Miscellanous steps import handle
    """

    portal = context.getSite()
    if context.readDataFile('onegov.edu-various.txt') is not None:
        configure_simplelayout(portal)
