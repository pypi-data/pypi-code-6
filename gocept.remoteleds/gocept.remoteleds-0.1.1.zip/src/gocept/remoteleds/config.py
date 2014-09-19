#!/usr/bin/python
# coding: utf-8


import os.path as op

import ConfigParser
import gocept.remoteleds.client


CONFIG = "config"
SNR = "SNR"
LEDCOUNT = "ledcount"
BASEURL = "baseurl"
TYPE = "type"
USER = "user"
PASSWORD = "password"
JENKINS = "jenkins"


class Config(object):

    def __init__(self, path='config.ini'):
        self.path = path

    def load(self):
        if op.isfile(self.path):
            self.config = ConfigParser.SafeConfigParser()
            self.config.read(self.path)
            sections = self.config.sections()
            self.client_names = [s for s in sections if s != CONFIG]
            print "Sections: %s" % sections
            print "Clients:  %s" % self.client_names

            self.read_base_configuration()
            self.read_client_configurations()
        else:
            raise IOError("No config file named {} found! See example.ini to get started!".format(self.path))

    def read_base_configuration(self):
        self.serial_number = self.config.get(CONFIG, SNR)
        self.led_count = int(self.config.get(CONFIG, LEDCOUNT))
        print "SNR: %s, led_count: %s" % (self.serial_number, self.led_count)

    def read_client_configurations(self):
        self.clients = []
        for name in self.client_names:
            typ, baseurl, user, password = self.read_client_configuration(name)
            projects = self.read_client_projects(name)
            self.clients.append({
                'type': typ, 'baseurl': baseurl,
                'user': user, 'password': password, 'projects': projects})

    def read_client_configuration(self, name):
        typ = self.config.get(name, TYPE)
        baseurl = self.config.get(name, BASEURL)

        user = None
        password = None
        if (self.config.has_option(name, USER)
                and self.config.has_option(name, PASSWORD)):
            user = self.config.get(name, USER)
            password = self.config.get(name, PASSWORD)

        return typ, baseurl, user, password

    def read_client_projects(self, name):
        projects = []
        led_numbers = range(0, self.led_count)
        for led_nr in led_numbers:
            led_name = "led{}".format(led_nr)
            if self.config.has_option(name, led_name):
                project = self.config.get(name, led_name)
                projects.append(
                    gocept.remoteleds.client.Project(name=project, led=led_nr))
        return projects

    def __str__(self):
        return "Config(SNR={},led_count={},clients={})".format(
            self.SNR, self.led_count, self.clients)
