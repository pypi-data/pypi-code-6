
import api
import logging
import json
from datetime import date

ENDPOINT_VERSIONS = "apps/{0}/app_versions"

KEY_ID = "id"
KEY_APP_VERSIONS = "app_versions"
KEY_VERSION_NO = "version"
KEY_MANDATORY = "mandatory"
KEY_CONFIG_URL = "config_url"
KEY_DOWNLOAD_URL = "download_url"
KEY_TIMESTAMP = "timestamp"
KEY_APPSIZE = "appsize"
KEY_DEVICE_FAMILY = "device_family"
KEY_NOTES = "notes"
KEY_STATUS = "status"
KEY_SHORT_VERSION = "shortversion"
KEY_MIN_OS = "minimum_os_version"
KEY_TITLE = "title"

def versions_endpoint(publicid):
    return ENDPOINT_VERSIONS.format(publicid)

def get_versions(publicid,page=None):
    logging.debug("Retrieving versions for public app id {0}".format(publicid))

    versions = []
    res = api.request(versions_endpoint(publicid))

    if res is None:
        return None

    rows = res[KEY_APP_VERSIONS]
    for row in rows:
        versions.append(Version(row))

    return versions

def get_version(publicid,versionid):
    logging.debug("Retrieving version with id {0}".format(versionid))

    versions = get_versions(publicid)
    for version in versions:
        if version.id() == versionid:
            return version
    return None

class Version:

    __id = None
    __title = None
    __versionNo = None
    __mandatory = None
    __configUrl = None
    __downloadUrl = None
    __timestamp = None
    __appsize = None
    __deviceFamily = None
    __notes = None
    __status = None
    __shortVersion = None
    __minOs = None

    def __init__(self,json):
        self.__id = str(json[KEY_ID])
        self.__title = json[KEY_TITLE]
        self.__versionNo = json[KEY_VERSION_NO]
        self.__mandatory = json[KEY_MANDATORY]
        self.__configUrl = json[KEY_CONFIG_URL] if json.has_key(KEY_CONFIG_URL) else None
        self.__downloadUrl = json[KEY_DOWNLOAD_URL] if json.has_key(KEY_DOWNLOAD_URL) else None
        self.__timestamp = str(json[KEY_TIMESTAMP])
        self.__appsize = json[KEY_APPSIZE]
        self.__deviceFamily = json[KEY_DEVICE_FAMILY]
        self.__notes = json[KEY_NOTES]
        self.__status = json[KEY_STATUS]
        self.__shortVersion = json[KEY_SHORT_VERSION]
        self.__minOs = json[KEY_MIN_OS]

    def __cmp__(self,other):
        return self.versionNo() == other.versionNo()

    def __str__(self):
        return json.dumps(self.arr(), sort_keys=True, indent=4, separators=(',', ': '))

    def arr(self):
        return { \
            KEY_ID:self.__id, \
            KEY_TITLE:self.__title, \
            KEY_VERSION_NO:self.__versionNo, \
            KEY_MANDATORY:self.__mandatory, \
            KEY_CONFIG_URL: self.__configUrl, \
            KEY_DOWNLOAD_URL: self.__downloadUrl, \
            KEY_TIMESTAMP: self.__timestamp, \
            KEY_APPSIZE: self.__appsize, \
            KEY_DEVICE_FAMILY: self.__deviceFamily, \
            KEY_NOTES: self.__notes, \
            KEY_STATUS: self.__status, \
            KEY_SHORT_VERSION: self.__shortVersion, \
            KEY_MIN_OS: self.__minOs
        }

    def id(self):
        return self.__id

    def title(self):
        return self.__title

    def versionNo(self):
        return self.__versionNo

    def mandatory(self):
        return self.__mandatory

    def configUrl(self):
        return self.__configUrl

    def downloadUrl(self):
        return self.__downloadUrl

    def timestamp(self):
        return self.__timestamp

    def appsize(self):
        return self.__timestamp

    def deviceFamily(self):
        return self.__deviceFamily

    def notes(self):
        return self.__notes

    def status(self):
        return self.__status

    def shortVersion(self):
        return self.__shortVersion

    def minOs(self):
        return self.__minOs