import logging

from config import PSQL_URI, ESI_VERSION

# Detect if additional apps are installed 
# ityou.astream
try:
    from ityou.astream.dbapi import DBApi 
    db_astream = DBApi()
    logging.info("ityou.intranet says: Activity Stream App is installed - Great!")
except:
    db_astream = None
    logging.info("ityou.intranet says: Unfortunately Activity Stream App not installed - Activities will not be tracked")

#ityou.imessage
try:
    from ityou.imessage.dbapi import DBApi
    from ityou.imessage.portlets.utils import InstantMessageUtils  
    db_imessage = DBApi()
    imessage_utils = InstantMessageUtils()
    logging.info("ityou.intranet says: Instant Message App is installed - Great!")
except:
    db_imessage = None
    imessage_utils = None
    logging.info("ityou.intranet says: Unfortunately Instant Message App not installed - Messages will not be tracked")

#ityou.whoisonline
try:
    from ityou.whoisonline.dbapi import DBApi 
    db_whoisonline = DBApi()
    logging.info("ityou.intranet says: WhoIsOnline App is installed - Great!")
except:
    db_whoisonline = None
    logging.info("ityou.intranet says: Unfortunately WhoIsOnline App not installed - You will not see who is online")

#ityou.extuserprofile
try:
    import ityou.extuserprofile
    logging.info("ityou.intranet says: extuserprofile  App is installed - Great!")
    ityou_extuserprofile_installed = True
except:
    ityou_extuserprofile_installed = False
    logging.info("ityou.intranet says: Unfortunately extuserprofile App not installed - You will not see extended user profiles")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""



