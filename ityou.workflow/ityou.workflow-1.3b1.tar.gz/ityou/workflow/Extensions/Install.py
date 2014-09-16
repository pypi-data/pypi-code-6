from StringIO import StringIO
import logging
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

from ityou.workflow import INDEX, INDEX_OFF, TODO

def uninstall_todo_view(self):
    """Removes the todo view and 
    reinstall index_html (from index_html_OFF, if any)
    """
    portal  = getSite()
    mt      = getToolByName(portal, 'portal_membership')
    ut = getToolByName(portal, "portal_url")
    portal = ut.getPortalObject()

    if hasattr(portal, TODO):
        todo_folder = getattr(portal, TODO)
        if todo_folder.getLayout() ==  '@@todo':
            todo_folder.setLayout('folder_listing')
            logging.info( "Reset layout to %s" % todo_folder.getLayout())
    
        if hasattr(todo_folder,INDEX_OFF):
            todo_folder.manage_renameObject(INDEX_OFF, INDEX)
            logging.info( "Renamed %s to %s" % (INDEX_OFF, INDEX) )

    
def uninstall(self):
    """We need to uninstall the views
    """
    out = StringIO()
    logging.info('Uninstalling ityou.workflow')
        
    uninstall_todo_view(self) 

    print >> out, "Successfully uninstalled ityou.workflow"

    return out.getvalue()

    
