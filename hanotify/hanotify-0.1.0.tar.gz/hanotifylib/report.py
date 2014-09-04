import mandrill
import os
import json

from hockeylib import crash
from hockeylib.crash import Crash

__MANDRILL_API_KEY = "LE_v3JWGdGh6sKLQE_ZeMw"

KEY_PREHEADER = "PREHEADER_CONTENT"
KEY_APP_TITLE = "APP_TITLE"
KEY_VERSION_CODE = "VERSION_CODE"
KEY_CRASH_DATE = "CRASH_DATE"
KEY_CRASH_COUNT = "CRASH_COUNT"
KEY_CRASH_CLASS = "CRASH_CLASS"
KEY_CRASH_METHOD = "CRASH_METHOD"
KEY_CRASH_REASON = "CRASH_REASON"
KEY_CRASH_LINK = "CRASH_LINK"

KEY_NAME = "name"
KEY_CONTENT = "content"

HISTORY_FILENAME = "report_history.json"

def crash_link(crash):
    return "https://rink.hockeyapp.net/manage/apps/{0}/app_versions/{1}/crash_reasons/{2}".format(crash.appId(),crash.appVersion(),crash.id())

def merge_var(key,val):
    return {KEY_NAME:key,KEY_CONTENT:val}

def send_report(crash,app):

    preheader_content = "{0} Crashes Have Occured on {1}".format(crash.crashCount(),app.title())
    merge_vars = [
        merge_var(KEY_PREHEADER,preheader_content),
        merge_var(KEY_APP_TITLE,app.title()),
        merge_var(KEY_VERSION_CODE,crash.appVersionShort()),
        merge_var(KEY_CRASH_DATE,crash.lastCrash()),
        merge_var(KEY_CRASH_COUNT,crash.crashCount()),
        merge_var(KEY_CRASH_CLASS,crash.cclass()),
        merge_var(KEY_CRASH_METHOD,crash.method()),
        merge_var(KEY_CRASH_REASON,crash.reason()),
        merge_var(KEY_CRASH_LINK,crash_link(crash))
    ]

    mandrill_client = mandrill.Mandrill(__MANDRILL_API_KEY)

    message = {
        'from_email': 'administrator@astonclub.com.au',
        'from_name': 'Hanotify',
        'important': False,
        'global_merge_vars':merge_vars,
        'subject': 'Hanotify Crash Report',
        'tags': ["Hanotify", "Crash Report"],
        'to': [{'email': 'benjamin.wallis@loke.com.au',
                 'name': 'Benjamin Wallis',
                 'type': 'to'}]}

    result = mandrill_client.messages.send_template(
        template_name="hanotify-crash-report",
        template_content=[],
        message=message, 
        async=False, 
        ip_pool='Main Pool')

    save_report(crash)

def history_file_path():
    return os.path.expanduser("~/Documents/hanotify/{0}".format(HISTORY_FILENAME))

def save_report(crash):
    history = get_report_history()
    history.append(crash)

    with open(history_file_path(), "wb") as f:
        data = []
        for rec in history:
            data.append(rec.arr())
        f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

def has_record(crash):
    history = get_report_history()
    for rec in history:
        if rec.id() == crash.id():
            return True
    return False

def get_report_history():
    path = history_file_path()
    if not os.path.isfile(path):
        with open(path,"wb") as f:
            f.write("[]")

    history = []
    with open(path,"rb") as f:
        for row in json.load(f):
            history.append(Crash(row))
    return history