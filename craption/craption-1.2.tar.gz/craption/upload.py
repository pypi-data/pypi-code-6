#coding: utf-8

from craption import settings
import base64
import dropbox as dropbox_lib
import requests
from sfs_upload import sfs_upload
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
        elif to == "sfs":
                return(sfs(path, filename, conf['upload'].get('sfs_host')))


def dropbox(local_path, filename, dropconf):
    print (dropconf)
    client = dropbox_lib.client.DropboxClient(dropconf['token'])
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

def sfs(path, filename, host):
    fh = open(path, 'rb')
    return sfs_upload.upload(host, fh, filename)
