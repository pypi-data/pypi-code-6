# Setup handlers

# Setup handlers

import logging
from Products.CMFCore.utils import getToolByName
# The profile id of your package:
PROFILE_ID = 'profile-collective.slideshow:default'

def add_slideshow_folders(context, logger=None):
    if logger is None:
        logger = logging.getLogger('collective.slideshow')
    
    setup = getToolByName(context, 'portal_setup')
    catalog = getToolByName(context, 'portal_catalog')

    results = catalog.searchResults(path = {'query': '/'}, type = ['Dexterity Container'])

    print "Add slideshow folders"

    for item in results:
        if item.portal_type not in ['Folder', 'Image'] and item.is_folderish:
            object_folderish = item.getObject()
            try:
                if 'slideshow' not in object_folderish.objectIds():
                    object_folderish.invokeFactory(type_name="Folder", id="slideshow", title="slideshow")
                    folder = object_folderish['slideshow']
                    folder.showinsearch = False
                    folder.reindexObject()
                    folder.portal_workflow.doActionFor(folder, "publish", comment="Slideshow content automatically published")
                    print "Added slideshow folder to object"
            except:
                pass



def import_various(context):
    """Import step for configuration that is not handled in xml files.
    """
    # Only run step if a flag file is present
    if context.readDataFile('collective_slideshow-default.txt') is None:
        return
    logger = context.getLogger('collective.slidehsow')
    site = context.getSite()

    add_slideshow_folders(site, logger)
