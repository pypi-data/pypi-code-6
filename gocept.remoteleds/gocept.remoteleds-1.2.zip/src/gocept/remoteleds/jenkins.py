from .client import Client
from .log import log
import requests


class JenkinsClient(Client):

    def get_status(self, project):
        url = "{}/job/{}/api/json".format(self.baseurl, project.name)
        if self.user and self.passwd:
            response = requests.get(url, auth=(self.user, self.passwd))
        else:
            response = requests.get(url)
        try:
            return response.json()['color']
        except:
            log.error('Error while returning job result.')
            raise

    def get_state_for_project(self, project):
        #import random
        #if random.randint(0, 1):
        #    return 'blue'
        #else:
        #    return 'red'
        try:
            state = self.get_status(project)
            return state
        except Exception as e:
            log.error('Error while requesting data from jenkins: {}'.format(
                str(e)))
            return 'violet'



    def get_color_for_state(self, state):
        on = 32
        if 'ani' in state:
            on = 8
        if 'red' in state:
            return on, 0, 0
        elif 'blue' in state:
            return 0, on, 0
        elif 'yellow' in state:
            return on, on, 0
        elif 'violet' in state:
            return on/2, 0, on
        else:
            return 0, 0, on

    def get_sound_for_state(self, state):
        if 'blue' in state:
            return 'fixed'
        else:
            return 'broken'


class JenkinsViewClient(JenkinsClient):
    def get_status(self, project):
        if project.name == '':
            url = "{}/api/json".format(self.baseurl)
        else:
            url = "{}/view/{}/api/json".format(self.baseurl, project.name)
        if self.user and self.passwd:
            response = requests.get(url, auth=(self.user, self.passwd))
        else:
            response = requests.get(url)
        try:
            result = response.json()
            for job in result['jobs']:
                jobstate = job.get('color', 'red')
                if 'red' in jobstate or 'yellow' in jobstate:
                    return 'red'
            return 'blue'
        except:
            log.error('Error while returning job result.')
            log.error(response.text)
            raise
