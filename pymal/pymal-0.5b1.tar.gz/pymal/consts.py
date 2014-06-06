__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

__all__ = ['USER_AGENT', 'XMLS_DIRECTORY', 'HOST_NAME', 'DEBUG',
           'RETRY_NUMBER', 'RETRY_SLEEP', 'LONG_SITE_FORMAT_TIME',
           'SHORT_SITE_FORMAT_TIME', 'LONG_SITE_FORMAT_TIME',
           'MALAPPINFO_FORMAT_TIME', 'MALAPPINFO_NONE_TIME', 'MALAPI_FORMAT_TIME',
           'MALAPI_NONE_TIME']


USER_AGENT = 'api-indiv-0829BA2B33942A4A5E6338FE05EFB8A1'
XMLS_DIRECTORY = 'XML_TEMPLATES'

HOST_NAME = "http://myanimelist.net"

DEBUG = True
RETRY_NUMBER = 4
RETRY_SLEEP = 1

SHORT_SITE_FORMAT_TIME = '%b %Y'
LONG_SITE_FORMAT_TIME = '%b %d, %Y'
MALAPPINFO_FORMAT_TIME = "%Y-%m-%d"
MALAPPINFO_NONE_TIME = "0000-00-00"
MALAPI_FORMAT_TIME = "%Y%m%d"
MALAPI_NONE_TIME = "00000000"
