from zope.interface import Attribute
from zope.interface import Interface


class IDownloadTokenStorage(Interface):
    """Download token storage manager"""

    def get_storage():
        """Get storage from annoations"""

    def add(obj, email):
        """Extend storage by a new token"""

    def remove(downloadtoken):
        """Remove token from storage"""

    def get_downloadtoken(token):
        """Get downloadtoken by token"""

    def url(downloadtoken):
        """Generate the url based on a downloadtoken"""


class IDownloadlinkSent(Interface):
    """An event that can be fired to send notifications.
    """

    emails = Attribute("")
    comment = Attribute("")


class IDownloadlinkOpened(Interface):
    """An event that can be fired if someone opens a download link.
    """

    email = Attribute("")
