
import json
import api
import logging
import pycurl
import version
import crash

ENDPOINT_APPS = "apps"
ENDPOINT_UPLOAD = ENDPOINT_APPS+"/upload"

KEY_APPS = "apps"
KEY_TITLE = "title"
KEY_ID = "id"
KEY_BUNDLE_ID = "bundle_identifier"
KEY_PUBLIC_ID = "public_identifier"
KEY_DEVICE_FAMILY = "device_family"
KEY_MIN_OS = "minimum_os_version"
KEY_RELEASE_TYPE = "release_type"
KEY_STATUS = "status"
KEY_PLATFORM = "platform"
KEY_CONFIG_URL = "config_url"
KEY_PUBLIC_URL = "public_url"
KEY_IPA = "ipa"
KEY_ERRORS = "errors"

def get_all_apps():
    logging.debug("Requesting App List From Hockey App...")

    apps = []
    res = api.request(ENDPOINT_APPS)

    if res is None:
        return None

    if res.has_key(KEY_ERRORS):
        logging.error("Invalid HockeyApp API token given. Aborting...")
        return None

    rows = res[KEY_APPS]
    for row in rows:
        apps.append(App(row))
    return apps

def upload_app(file):
    logging.debug("Uploading build to HockeyApp...")

    postdata = [(KEY_IPA, (pycurl.FORM_FILE,file))]
    response = api.request(ENDPOINT_UPLOAD,postdata)

    if response is None:
        return None

    app = App(response)

    logging.debug("Build successfully uploaded for {0}".format(app.title()))

def get_app(appid=None,title=None):
    logging.debug("Retriving Hockey app with id {0}".format(appid))

    all_apps = get_all_apps()
    if all_apps is None:
        return None

    for app in all_apps:
        if title != None and app.title() == title:
            return app
        if appid != None and app.id() == appid:
            return app

    return None

class App:

    __id = None
    __title = None
    __bundleID = None
    __publicID = None
    __deviceFamily = None
    __minOs = None
    __releaseType = None
    __status = None
    __platform = None
    __configUrl = None
    __publicUrl = None

    def __init__(self,json):
        self.__id = str(json[KEY_ID])
        self.__title = json[KEY_TITLE]
        self.__bundleID = json[KEY_BUNDLE_ID]
        self.__publicID = json[KEY_PUBLIC_ID]
        self.__deviceFamily = json[KEY_DEVICE_FAMILY]
        self.__minOs = json[KEY_MIN_OS]
        self.__releaseType = json[KEY_RELEASE_TYPE]
        self.__status = json[KEY_STATUS]
        self.__platform = json[KEY_PLATFORM]
        self.__configUrl = json[KEY_CONFIG_URL] if json.has_key(KEY_CONFIG_URL) else None
        self.__publicUrl = json[KEY_PUBLIC_ID] if json.has_key(KEY_PUBLIC_ID) else None

    def __eq__(self,other):
        return other != None and (self.bundleID() == other.bundleID())

    def __str__(self):
        return json.dumps(self.arr(), sort_keys=True, indent=4, separators=(',', ': '))

    def arr(self):
        return {
            KEY_ID : self.__id,
            KEY_TITLE : self.__title,
            KEY_BUNDLE_ID : self.__bundleID,
            KEY_PUBLIC_ID : self.__publicID,
            KEY_DEVICE_FAMILY : self.__deviceFamily,
            KEY_MIN_OS : self.__minOs,
            KEY_RELEASE_TYPE : self.__releaseType,
            KEY_STATUS : self.__status,
            KEY_PLATFORM : self.__platform,
            KEY_CONFIG_URL : self.__configUrl,
            KEY_PUBLIC_URL : self.__publicUrl
        }

    def versions(self):
        return version.get_versions(self.__publicID)

    def current_version(self):
        return self.versions()[0]

    def crashes(self,versionCode=None,limit=crash.DEFAULT_LIMIT,sort=crash.SORT_OPTIONS[0],order=crash.ORDER_OPTIONS[0]):
        return crash.get_crashes(publicid=self.__publicID,version=versionCode,limit=limit,sort=sort,order=order)

    def id(self):
        return self.__id

    def title(self):
        return self.__title

    def bundleID(self):
        return self.__bundleID

    def publicID(self):
        return self.__publicID

    def deviceFamily(self):
        return self.__deviceFamily

    def minOS(self):
        return self.__minOs

    def releaseType(self):
        return self.__releaseType

    def status(self):
        return self.__status

    def platform(self):
        return self.__platform

    def configUrl(self):
        return self.__configUrl

    def publicUrl(self):
        return self.__publicUrl
