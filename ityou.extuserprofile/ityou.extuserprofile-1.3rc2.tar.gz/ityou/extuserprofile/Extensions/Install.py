from StringIO import StringIO
import logging
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

from ityou.extuserprofile import INDEX, INDEX_OFF

def uninstall_memberfolder_view(self):
    """Removes the userprofile view and 
    reinstall index_html (from index_html_OFF, if any)
    """
    portal  = getSite()
    mt      = getToolByName(portal, 'portal_membership')
    mfolder = mt.getMembersFolder()

    if mfolder.getLayout() ==  '@@users':
        mfolder.setLayout('folder_listing')
        logging.info( "Reset layout to %s" % mfolder.getLayout())

    if hasattr(mfolder,INDEX_OFF):
        mfolder.manage_renameObject(INDEX_OFF, INDEX)
        logging.info( "Renamed %s to %s" % (INDEX_OFF, INDEX) )

    
def uninstall(self):
    """We need to uninstall the views
    """
    out = StringIO()
    logging.info('Uninstalling ityou.extuserprofile')
        
    uninstall_memberfolder_view(self) 

    print >> out, "Successfully uninstalled ityou.extuserprofile"

    return out.getvalue()

    
