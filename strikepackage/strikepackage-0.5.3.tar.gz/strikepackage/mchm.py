import json
import time

from requests import Request, Session
import requests.exceptions
from jinja2 import Environment, FileSystemLoader
from progress.spinner import Spinner

from .utils import abort, warn


def mchm_render(template_dir, params):
    """
    Renders templates
    """
    env = Environment(loader=FileSystemLoader(template_dir))
    userdata = None
    metadata = None
    try:
        userdata = env.get_template('userdata.jinja2').render(params=params)
        metadata = env.get_template('metadata.jinja2').render(params=params)
    except IOError as ex:
        abort("Couldn't open template file: {}".format(ex.message))
    return userdata, metadata


def mchm_api_call(url, method, **kwargs):
    """
    Generic method to make HTTP requests to MCHM
    """
    attempt = 0
    resp = None
    method = method.upper()
    if method not in ['HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
        raise requests.exceptions.RequestException('Unknown method')

    s = Session()
    req = Request(method, url, **kwargs)
    prepped = s.prepare_request(req)

    while True:
        try:
            attempt += 1
            resp = s.send(prepped, verify=True)
            resp.raise_for_status()
            break
        except (requests.HTTPError, requests.ConnectionError,
                requests.Timeout) as ex:
            if attempt >= 5:
                abort(ex.message)
            else:
                continue
        except requests.URLRequired as ex:
            abort(ex.message)
    return resp


def mchm_upload(mchm_url, userdata, metadata, iid=None):
    """
    Uploads templates to MCHM server
    """
    url = "{}/api/submit".format(mchm_url)
    headers = {'content-type': 'application/json'}
    if iid is not None:
        uploadtype = ('id', iid)
    else:
        uploadtype = ('install-type', 'cloud-init')
    payload = json.dumps({
        uploadtype[0]: uploadtype[1],
        'user-data': userdata,
        'meta-data': metadata,
    })
    resp = mchm_api_call(url, 'post', data=payload, headers=headers)
    if resp is not None:
        return resp.json()
    else:
        abort("ERROR: MCHM upload error")
        return None


def mchm_poll(mchm_url, mchm_id, max_poll_time):
    """
    Poll MCHM server looking for Phonehome
    """
    url = "{}/api/phonehome/{}".format(mchm_url, mchm_id)
    timer = 0
    spinner = Spinner("Waiting for cloud-init phonehome... ")
    while timer < max_poll_time:
        resp = (mchm_api_call(url, 'get')).json()
        if resp['phonehome_status']:
            print "\nPhone Home detected."
            break
        spinner.next()
        time.sleep(1)
        timer += 1
    else:
        warn("Poll max time exceeded. VM took too long to phone home.")
    spinner.finish()
    return