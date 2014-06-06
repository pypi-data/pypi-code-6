import logging

import re
import requests
import base64
import os
import json

from subprocess import Popen
from docker.auth.auth import load_config

from sbdk.auth import login
from sbdk.error import SbdkError



DOCKER_CONFIG_FILENAME = '.dockercfg'
ALLOWED_CHARS_RE = re.compile('^[a-z0-9]$')


def dockerize(username):
    return ''.join([chr if re.match(ALLOWED_CHARS_RE, chr) else '_' for chr in username.lower()])

# def dockerize(username):
#    return ''.join([c.lower() if (c.isalnum() or c == '_') else '' for c in username])  .decode('utf-8').encode('idna')


def repo_name(project, user):
    saved_user = project.state.get('username')
    if not saved_user:
        saved_user = dockerize(user)
        project.state['username'] = saved_user
        project.state.save()
    ret = project.docker_registry_name + '/' + saved_user + '/' + project.name
    return ret


def store_credentials(docker_registry_name, username, password, cfg, email=None):
    email = email or '%s@example.com' % username

    def convert_to_dockercfg(cfg):
        def encode_auth(username, password):
            return base64.b64encode(username + b':' + password)

        dockercfg = {}
        for repo, auth in cfg.iteritems():
            dockercfg[repo] = {'auth': encode_auth(auth['username'], auth['password']), 'email': auth['email']}
        return dockercfg

    config_file = os.path.join(os.environ.get('HOME', '.'), DOCKER_CONFIG_FILENAME)
    if not cfg.get(docker_registry_name, None):
        cfg[docker_registry_name] = {}
    cfg[docker_registry_name]['username'], cfg[docker_registry_name]['password'], cfg[docker_registry_name]['email'] \
        = username, password, email

    with open(config_file, 'w') as outfile:
        json.dump(convert_to_dockercfg(cfg), outfile)


class Container(object):

    def __init__(self, docker_client, project, container,
                 image=None, message=None, user=None, token=None, repository=None):
        self.docker = docker_client
        self.container = container
        self.project = project
        self.image = image
        self.message = message
        self._user = user
        self._token = token
        self._repository = repository

    @property
    def user(self):
        if not self._user:
            self.load_credentials()
        return self._user

    @property
    def token(self):
        if not self._token:
            self.load_credentials()
        return self._token

    @property
    def repository(self):
        if not self._repository:
            self._repository = repo_name(self.project, self.user)
        return self._repository

    def inspect(self):
        return self.docker.inspect_container(self.container)

    def is_running(self):
        return self.inspect()['State']['Running']

    def wait(self):
        if self.is_running():
            self.docker.wait(self.container)
        return self

    def is_success(self):
        self.wait()
        return self.inspect()['State']['ExitCode'] == 0

    def remove(self):
        self.wait()
        self.docker.remove_container(self.container)

    def stop(self, nice=False):
        return self.docker.stop(self.container) if nice else self.docker.kill(self.container)

    def print_log(self):
        if self.is_running():
            for out in self.docker.attach(container=self.container, stream=True):
                print(out.rstrip())
        else:
            print(self.docker.logs(self.container))

    def commit(self, message=None, config=None, tag=True):
        if message:
            self.message = message

        self.image = self.docker.commit(self.container['Id'], message=message, conf=config)
        if tag and self.project.name and self.user:
            self.docker.tag(self.image['Id'], self.repository, tag=self.tag)
        else:
            print("Image ID:", self.tag)
        return self

    def save_as_base(self):
        if not self.image:
            raise SbdkError("Container image not committed yet!")
        self.project.state['image_id'] = self.image['Id']
        self.project.state.save()

    def push(self):
        if not self.image:
            raise SbdkError("Container image not committed yet!")

        self.docker.push(self.repository)

    def load_credentials(self, renew=False):
        cfg = load_config()
        if renew or not cfg:
            self._user, self._token = login(self.project)
            store_credentials(self.project.docker_registry_url, self._user, self._token, cfg)

        else:
            self._user = cfg['username']
            self._token = cfg['password']

    @property
    def tag(self):
        return self.image['Id'][:16]