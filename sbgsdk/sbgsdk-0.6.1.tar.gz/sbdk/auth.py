import getpass
import json
import requests
import logging
import os
import getpass
import base64

from sbdk.error import SbdkError

DOCKER_CONFIG_FILENAME = '.dockercfg'

def login(project, retries=2):
    if retries < 0:
        raise SbdkError('Login failed')
    url = project.schema_server_url + '/auth'
    usr = raw_input("Username: ")
    if not usr:
        return login(project, retries-1)
    pwd = getpass.getpass()
    resp = push_json(url, {'username': usr, 'password': pwd}, None, no_raise_for=[401, 402])
    if resp.status_code in (401, 402):
        print('Sorry. Try again.')
        return login(project, retries-1)
    return usr, resp.json()['session_id']


def push_url(project, user):
    return project.schema_server_url + '/repo/' + user + '/' + project.name + '/image'


def push_json(url, data, session_id, no_raise_for=tuple()):
    headers = {'Content-Type': 'application/json'}
    if session_id:
        headers['session-id'] = session_id
    response = requests.post(url, json.dumps(data), headers=headers, verify=False)
    if response.status_code not in no_raise_for:
        response.raise_for_status()
    return response


def store_credentials(docker_registry_name, username, password, cfg, email=None):
    email = email or '%s@example.com' % username

    if not cfg.get(docker_registry_name, None):
        cfg[docker_registry_name] = {}
    cfg[docker_registry_name]['username'], cfg[docker_registry_name]['password'], cfg[docker_registry_name]['email'] \
        = username, password, email
    update_docker_cfg(cfg)


def update_docker_cfg(cfg):
    def convert_to_dockercfg(cfg):
        def encode_auth(username, password):
            return base64.b64encode(username + b':' + password)
        dockercfg = {}
        for repo, auth in cfg.iteritems():
            dockercfg[repo] = {'auth': encode_auth(auth['username'], auth['password']), 'email': auth['email']}
        return dockercfg

    config_file = os.path.join(os.environ.get('HOME', '.'), DOCKER_CONFIG_FILENAME)
    with open(config_file, 'w') as outfile:
        json.dump(convert_to_dockercfg(cfg), outfile)