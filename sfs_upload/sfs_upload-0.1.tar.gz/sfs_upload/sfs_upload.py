from uuid import uuid1
import os
import requests
import sys

def upload(host, fh, name):
    uuid = uuid1()
    upload_url = "http://{0}/upload".format(host)
    merge_url = "http://{0}/merge".format(host)

    get_params = {
        'uuid': uuid,
        'chunkIndex': 0,
    }

    requests.post(upload_url, params=get_params, data=fh)

    get_params = {
        'uuid': uuid,
        'chunkCount': 1,
        'name': name,
        'collectionID': uuid1(),
    }

    res = requests.post(merge_url, params=get_params).json()
    sfs_id = res['fileName']

    return "http://{0}/d/{1}".format(host, sfs_id)

if __name__ == '__main__':
    host = 'localhost:9898'
    path = sys.argv[1]
    name = os.path.basename(path)
    fh = open(path, 'rb')
    print(upload(host, fh, name))
