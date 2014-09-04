
import logging
import os
import json
from hockeylib import app
from hockeylib import version

WATCHLIST_FILENAME = "watching.json"

KEY_APP_NAME = "app_name"
KEY_APP_ID = "app_id"
KEY_APP_VERSION = "app_version"
KEY_THRESHOLD_COUNT = "threshold_count"

DEFAULT_THRESHOLD = 50

def watchlist_file():
    return os.path.expanduser("~/Documents/hanotify/{0}".format(WATCHLIST_FILENAME))

def get_watchlist():

    path = watchlist_file()
    if not os.path.isfile(path):
        with open(path,"wb") as f:
            f.write("[]")

    watchlist = []
    with open(path,"rb") as f:
        for row in json.load(f):
            watchlist.append(Watch(row))
    return watchlist

def get_watch(appid,versionid):
    watch_list = get_watchlist()

    for watch in watch_list:
        if watch.appId() == appid and watch.appVersion() == versionid:
            return watch

    return None

def watch_app(appid,versionid=None,countThreshold=DEFAULT_THRESHOLD):
    logging.debug("Configuring hanotify to watch {0}".format(appid))

    # Checking if the app exists
    new_app = app.get_app(appid=appid)
    if new_app == None:
        logging.error("Unable to find the specified hockeyapp")
        return False

    # Grabbing the recent version id of the app
    if versionid == None:
        versionid = new_app.current_version().id()

    # Checking if the version exists
    if version.get_version(new_app.publicID(),versionid) is None:
        logging.error("Application version does not exist")
        return False

    # Checking if the watch already exists
    if not get_watch(appid,versionid) is None:
        logging.error("Application is already configured to be watched")
        return False

    # Adding the watch to the list
    watch_list = get_watchlist()
    new_watch = Watch(appId=appid,appName=new_app.title(),appVersion=versionid,countThreshold=countThreshold)
    watch_list.append(new_watch)
    save_watch_list(watch_list)

    logging.debug("Hanotify is now configured to watch {0}".format(appid))
    return True

def unwatch_app(appid):
    logging.debug("Removing {0} from hanotify watch list".format(appid))

    index = -1
    watch_list = get_watchlist()
    for watch in watch_list:
        if watch.appId() == appid:
            index = watch_list.index(watch)
            break

    if index == -1:
        logging.error("Hanotify is currently not watching that app.");
        return

    watch_list.pop(index)
    save_watch_list(watch_list)

    logging.debug("{0} has been successfully removed from the watch list".format(appid))
    return True

def save_watch_list(watchlist):
    with open(watchlist_file(), "wb") as f:
        data = []
        for watch in watchlist:
            data.append(watch.arr())
        f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

class WatchEncoder(json.JSONEncoder):
    def default(self,o):
        return o.arr()

class Watch:

    __appId = None
    __appName = None
    __appVersion = None
    __countThreshold = None

    def __init__(self,json=None,appId=None,appName=None,appVersion=None,countThreshold=DEFAULT_THRESHOLD):
        if json != None:
            self.__appName = json[KEY_APP_NAME]
            self.__appId = json[KEY_APP_ID]
            self.__appVersion = json[KEY_APP_VERSION]
            self.__countThreshold = json[KEY_THRESHOLD_COUNT]
        else:
            self.__appName = appName
            self.__appId = appId
            self.__appVersion = appVersion
            self.__countThreshold = countThreshold

    def __cmp__(self,other):
        return other != None and (self.appId() == other.appId()) and (self.appVersion() == other.appVersion())

    def __str__(self):
        return json.dumps(self.arr(), sort_keys=True, indent=4, separators=(',', ': '))

    def arr(self):
        return { 
            KEY_APP_NAME: self.__appName, 
            KEY_APP_ID: self.__appId, 
            KEY_APP_VERSION: self.__appVersion, 
            KEY_THRESHOLD_COUNT: self.__countThreshold 
        }

    def appId(self):
        return self.__appId

    def appName(self):
        return self.__appName

    def appVersion(self):
        return self.__appVersion

    def countThreshold(self):
        return self.__countThreshold
