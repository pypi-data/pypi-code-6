from requests import Session, Request
import requests.exceptions

from .utils import warn


def puppet_api_call(url, method, config, **kwargs):
    """
    Generic method to make Puppet HTTP API calls
    """
    attempt = 0
    max_attempt = 5
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
            resp = s.send(prepped, verify=config['puppet_cacert'],
                          cert=(config['puppet_cert'], config['puppet_key']))
            resp.raise_for_status()
            break
        except (requests.HTTPError, requests.ConnectionError,
                requests.Timeout, requests.URLRequired) as ex:
            if attempt >= max_attempt:
                warn("{}".format(ex.message))
                return None
            else:
                continue
    return resp


def puppet_findcsr(config, vm_fqdn):
    """
    Looks for a node CSR using the Puppet API
    """
    url = "{}/{}/certificate_status/{}".format(
        config['puppet_url'], config['puppet_environment'], vm_fqdn
    )
    headers = {'Accept': 'pson'}
    resp = puppet_api_call(url, 'get', config, headers=headers)
    if resp is not None:
        return resp.json()
    else:
        warn("Couldn't find node CSR.")
        return False


def puppet_signcsr(config, vm_fqdn):
    """
    Sign a node CSR
    """
    print "Attempting to sign node CSR..."
    pson = puppet_findcsr(config, vm_fqdn)

    # sanity check result a litle bit
    if not pson:
        return False

    try:
        if pson['state'] != 'requested':
            if pson['state'] == 'signed':
                warn("A certificate with this subject name has already "
                     "been signed.")
            else:
                warn("Certificate in unexpected "
                     "state: {}".format(pson['state']))
            return False
    except KeyError:
        warn("API returned unexpected data: {}".format(pson))
        return False

    # Sign node CSR
    url = "{}/{}/certificate_status/{}".format(config['puppet_url'],
                                               config['puppet_environment'],
                                               vm_fqdn)
    headers = {'Content-Type': 'text/pson'}
    payload = '{"desired_state": "signed"}'
    resp = puppet_api_call(url, 'put', config, headers=headers, data=payload)
    if resp is not None:
        print "Certificate signed. Node will run catalog at next interval."
        return True
    else:
        warn("Couldn't sign node CSR")
        return False