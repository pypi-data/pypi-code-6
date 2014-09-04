
import api
import json

KEY_CRASH_REASONS = "crash_reasons"
KEY_ID = "id"
KEY_STATUS = "status"
KEY_LINE = "line"
KEY_BUNDLE_VERSION = "bundle_version"
KEY_CRASH_COUNT = "number_of_crashes"
KEY_APP_VERSION = "app_version_id"
KEY_CREATED_AT = "created_at"
KEY_LAST_CRASH = "last_crash_at"
KEY_UPDATED_AT = "updated_at"
KEY_APP_ID = "app_id"
KEY_EXCEPTION_TYPE = "exception_type"
KEY_VERSION_SHORT = "bundle_short_version"
KEY_REASON = "reason"
KEY_FILE = "file"
KEY_METHOD = "method"
KEY_FIXED = "fixed"
KEY_CLASS = "class"

DEFAULT_LIMIT = 25
SORT_OPTIONS = ['date','class','number_of_crashes','last_crash_at']
ORDER_OPTIONS = ['asc','desc']

def crash_endpoint(publicid,version=None,limit=DEFAULT_LIMIT,sort=SORT_OPTIONS[0],order=ORDER_OPTIONS[0]):
    endpoint = None
    if version == None:
        endpoint = "apps/{0}/crash_reasons?per_page={1}&sort={2}&order={3}".format(publicid,limit,sort,order)
    else:
        endpoint = "apps/{0}/app_versions/{1}/crash_reasons?per_page={2}&sort={3}&order={4}".format(publicid,version,limit,sort,order)
    return endpoint

def get_crashes(publicid,version=None,limit=DEFAULT_LIMIT,sort=SORT_OPTIONS[0],order=ORDER_OPTIONS[0]):
    res = api.request(crash_endpoint(publicid,version,limit,sort,order))

    if res is None:
        return None

    rows = res[KEY_CRASH_REASONS]
    crashes = []
    for row in rows:
        crashes.append(Crash(row))
    return crashes

class Crash:

    __id = None
    __status = None
    __line = None
    __bundleVersion = None
    __crashCount = None
    __appVersion = None
    __createdAt = None
    __lastCrash = None
    __updatedAt = None
    __appId = None
    __exceptionType = None
    __appVersionShort = None
    __reason = None
    __file = None
    __method = None
    __fixed = None
    __class = None

    def __init__(self,json):
        self.__id = str(json[KEY_ID])
        self.__status = str(json[KEY_STATUS])
        self.__line = str(json[KEY_LINE])
        self.__bundleVersion = str(json[KEY_BUNDLE_VERSION])
        self.__crashCount = str(json[KEY_CRASH_COUNT])
        self.__appVersion = str(json[KEY_APP_VERSION])
        self.__createdAt = json[KEY_CREATED_AT]
        self.__lastCrash = json[KEY_LAST_CRASH]
        self.__updatedAt = json[KEY_UPDATED_AT]
        self.__appId = json[KEY_APP_ID]
        self.__exceptionType = json[KEY_EXCEPTION_TYPE]
        self.__appVersionShort = json[KEY_VERSION_SHORT]
        self.__reason = json[KEY_REASON]
        self.__file = json[KEY_FILE]
        self.__method = json[KEY_METHOD]
        self.__fixed = json[KEY_FIXED]
        self.__class = json[KEY_CLASS]

    def __str__(self):
        return json.dumps(self.arr(), sort_keys=True, indent=4, separators=(',', ': '))

    def __cmp__(self,other):
        return (not other is None) and (self.id() == other.id())

    def arr(self):
        return { \
            KEY_ID : self.__id, \
            KEY_STATUS : self.__status, \
            KEY_LINE : self.__line, \
            KEY_BUNDLE_VERSION : self.__bundleVersion, \
            KEY_CRASH_COUNT : self.__crashCount, \
            KEY_APP_VERSION : self.__appVersion, \
            KEY_CREATED_AT : self.__createdAt, \
            KEY_LAST_CRASH : self.__lastCrash, \
            KEY_UPDATED_AT : self.__updatedAt, \
            KEY_APP_ID : self.__appId, \
            KEY_EXCEPTION_TYPE : self.__exceptionType, \
            KEY_VERSION_SHORT : self.__appVersionShort, \
            KEY_REASON : self.__reason, \
            KEY_FILE : self.__file, \
            KEY_METHOD : self.__method, \
            KEY_FIXED : self.__fixed, \
            KEY_CLASS : self.__class 
        }

    def id(self):
        return self.__id

    def status(self):
        return self.__status

    def line(self):
        return self.__line

    def bundleVersion(self):
        return self.__bundleVersion

    def crashCount(self):
        return self.__crashCount

    def appVersion(self):
        return self.__appVersion

    def createdAt(self):
        return self.__createdAt

    def lastCrash(self):
        return self.__lastCrash

    def updatedAt(self):
        return self.__updatedAt

    def appId(self):
        return self.__appId

    def exceptionType(self):
        return self.__exceptionType

    def appVersionShort(self):
        return self.__appVersionShort

    def reason(self):
        return self.__reason

    def file(self):
        return self.__file

    def method(self):
        return self.__method

    def fixed(self):
        return self.__fixed

    def cclass(self):
        return self.__class
