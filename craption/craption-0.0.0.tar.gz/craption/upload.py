#coding: utf-8

import base64
import dropbox as dropbox_lib
import requests
from craption import settings
import subprocess

conf = settings.get_conf()
def upload(path, filename):
    if conf['upload']['upload']:
        to = conf['upload']['to'].lower()
        if to == "imgur":
                return(imgur(path, conf['upload']['imgur']['api-key']))
        elif to == "scp":
                return(scp(path, filename, conf['upload']['scp']))
        elif to == "dropbox":
                return(dropbox(path, filename, conf['upload']['dropbox']))


def dropbox(local_path, filename, dropconf):
    sess = dropbox_lib.session.DropboxSession(
        dropconf['app']['key'],
        dropconf['app']['secret'],
        "app_folder"
    )
    sess.set_token(
        dropconf['token']['key'],
        dropconf['token']['secret']
    )
    client = dropbox_lib.client.DropboxClient(sess)
    uploaded = client.put_file("/" + filename, open(local_path))
    return client.share(uploaded['path'])['url']

def imgur(path, api_key):
    img_data = base64.b64encode(open(path).read())
    data = {
        'key': api_key,
        'image': img_data
    }
#       data = urllib.urlencode(params)
#       req = urllib2.Request(url, data)
#       res = json.loads(urllib2.urlopen(req).read())["upload"]

    url = 'http://api.imgur.com/2/upload.json'
    res = requests.post(url, data=data).json()
    return res['upload']['links']['original']



def scp(local_file, filename, scpconf):
    cmd = [
        'scp',
        local_file,
        "%s@%s:%s/%s" % (
                            scpconf['user'],
                            scpconf['host'],
                            scpconf['path'],
                            filename        
                        ),
    ]
    nullw = open('/dev/null', 'w')
    nullr = open('/dev/null')
    p = subprocess.Popen(cmd, stdout=nullw, stdin=nullr, stderr=nullw)
    p.wait()
    return scpconf['url'].replace('{f}', filename)
