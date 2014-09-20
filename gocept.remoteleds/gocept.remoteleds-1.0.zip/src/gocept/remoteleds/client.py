import time
import random
from .log import log


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

    #update every x ticks
    update_ticks = 100
    support_state_changes = True

    def __init__(self, connection, config):
        self.baseurl = config['baseurl']
        self.user = config['user']
        self.passwd = config['password']
        self.projects = config['projects']
        self.connection = connection

    def get_state_for_project(self, project):
        """Implement in concrete client."""
        raise NotImplementedError()

    def get_color_for_state(self, state):
        """Implement in concrete client."""
        raise NotImplementedError()

    def get_sound_for_state(self, state):
        """Implement in concrete client."""
        raise NotImplementedError()

    def update(self, tick):
        if tick % self.update_ticks != 0:
            return
        log.debug("Update {}".format(self.__class__.__name__))
        for project in self.projects:
            state = self.get_state_for_project(project)
            project.push_state(state)
            log.debug("{}: {} (LED {})".format(
                project.name, project.state, project.led))
            self.send_state(self.connection, project)

    def send_state(self, connection, project):
        if (project.state != project.last_state
                and project.last_state is not None
                and self.support_state_changes):
            new_message = self.calculate_message_from_state(
                project.led, project.state)
            old_message = self.calculate_message_from_state(
                project.led, project.last_state)
            sound = self.get_sound_for_state(project.state)
            if sound is not None:
                connection.write('SND{}'.format(sound))
                connection.flushInput()
            for i in range(10):
                connection.write(new_message)
                connection.write("FLU\n")
                connection.flushInput()
                time.sleep(0.2)
                connection.write(old_message)
                connection.write("FLU\n")
                connection.flushInput()
                time.sleep(0.2)

        message = self.calculate_message_from_state(project.led, project.state)
        connection.write(message)
        connection.write("FLU\n")
        connection.flushInput()

    def calculate_message_from_state(self, led, state):
        red, green, blue = self.get_color_for_state(state)
        return "LED%02d%03d%03d%03d\n" % (led, red, green, blue)

