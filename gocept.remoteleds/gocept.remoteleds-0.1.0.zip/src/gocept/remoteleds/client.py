import requests
import time
import random


class Project(object):

    def __init__(self, name, led):
        self.name = name
        self.led = led
        self.state = None
        self.last_state = None

    def push_state(self, state):
        self.last_state = self.state
        self.state = state


class Client(object):

    def __init__(self, connection, baseurl, projects, user=None, passwd=None):
        self.connection = connection
        self.baseurl = baseurl
        self.projects = projects
        self.user = user
        self.passwd = passwd

    def get_state_for_project(self, project):
        """Implement in concrete client."""
        raise NotImplementedError()

    def get_color_for_state(self, state):
        """Implement in concrete client."""
        raise NotImplementedError()

    def get_sound_for_state(self, state):
        """Implement in concrete client."""
        raise NotImplementedError()

    def update(self):
        for project in self.projects:
            state = self.get_state_for_project(project)
            project.push_state(state)
            print("{}: {} (LED {})".format(
                project.name, project.state, project.led))
            self.send_state(self.connection, project)

    def send_state(self, connection, project):
        if (project.state != project.last_state
                and project.last_state is not None):
            new_message = self.calculate_message_from_state(
                project.led, project.state)
            old_message = self.calculate_message_from_state(
                project.led, project.last_state)
            sound = self.get_sound_for_state(project.state)

            connection.write('SND{}'.format(sound))
            connection.flushInput()
            for i in range(10):
                connection.write(new_message)
                connection.flushInput()
                time.sleep(0.2)
                connection.write(old_message)
                connection.flushInput()
                time.sleep(0.2)

        message = self.calculate_message_from_state(project.led, project.state)
        connection.write(message)
        connection.flushInput()

    def calculate_message_from_state(self, led, state):
        red, green, blue = self.get_color_for_state(state)
        return "LED%02d%03d%03d%03d\n" % (led, red, green, blue)


class JenkinsClient(Client):

    def get_state_for_project(self, project):
        url = "{}/job/{}/api/json".format(self.baseurl, project.name)
        if self.user and self.passwd:
            response = requests.get(url, auth=(self.user, self.passwd))
        else:
            response = requests.get(url)

        # if random.randint(0, 1):
        #     return 'blue'
        # else:
        #     return 'red'
        return response.json()['color']

    def get_color_for_state(self, state):
        if 'red' in state:
            return 128, 0, 0
        elif 'blue' in state:
            return 0, 128, 0
        elif 'yellow' in state:
            return 128, 128, 0
        else:
            return 0, 0, 128

    def get_sound_for_state(self, state):
        if 'blue' in state:
            return 'fixed'
        else:
            return 'broken'
