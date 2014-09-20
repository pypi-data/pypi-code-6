from .client import Client
import requests


class JenkinsClient(Client):

    def get_state_for_project(self, project):
        url = "{}/job/{}/api/json".format(self.baseurl, project.name)
        if self.user and self.passwd:
            response = requests.get(url, auth=(self.user, self.passwd))
        else:
            response = requests.get(url)

        #import random
        #if random.randint(0, 1):
        #    return 'blue'
        #else:
        #    return 'red'
        return response.json()['color']

    def get_color_for_state(self, state):
        if 'red' in state:
            return 32, 0, 0
        elif 'blue' in state:
            return 0, 32, 0
        elif 'yellow' in state:
            return 32, 32, 0
        else:
            return 0, 0, 32

    def get_sound_for_state(self, state):
        if 'blue' in state:
            return 'fixed'
        else:
            return 'broken'
