import logging

import re
import requests
from sys import stdout

from subprocess import Popen
from docker.auth.auth import load_config

from sbdk.auth import login, store_credentials
from sbdk.error import SbdkError


ALLOWED_CHARS_RE = re.compile('^[a-z0-9]$')


def dockerize(username):
    return ''.join([chr if re.match(ALLOWED_CHARS_RE, chr) else '_' for chr in username.lower()])


def repo_name(project, user):
    saved_user = project.state.get('username')
    if not saved_user:
        saved_user = dockerize(user)
        project.state['username'] = saved_user
        project.state.save()
    else:
        saved_user = dockerize(saved_user)
    ret = project.docker_registry_name + '/' + saved_user + '/' + project.name
    return ret


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
        push = Popen(['docker', 'push', self.repository], stdout=stdout)
        push.wait()

    def load_credentials(self, renew=False):
        cfg = load_config()
        session_id = cfg.get(self.project.docker_registry_url, None).get('password', None) if cfg.get(
            self.project.docker_registry_url, None) else None
        resp = requests.get(self.project.schema_server_url + '/auth', headers={"session-id": session_id}, verify=False)

        if renew or resp.status_code != 200:
            self._user, self._token = login(self.project)
            store_credentials(self.project.docker_registry_url, self._user, self._token, cfg)

        else:
            self._user = cfg[self.project.docker_registry_url]['username']
            self._token = cfg[self.project.docker_registry_url]['password']


    def check_privilege(self):
        if not self.project.state.get('username'):
            raise SbdkError("File state.json doesn't contain username")
        url = '%s/repo/%s/%s' %(self.project.schema_server_url, dockerize(self.project.state['username']),
                                self.project.state['project_name'])
        resp = requests.get(url, headers={"session-id": self._token}, verify=False)
        contributors = resp.json()['contributors'] if resp.json().get('contributors', None) else []
        if (resp.status_code == 404 and self.project.state.get('username') == self._user) or (
                        resp.status_code == 200 and (dockerize(self._user) == resp.json()['owner'] or self._user in contributors)):
            return True
        return False


    @property
    def tag(self):
        return self.image['Id'][:16]