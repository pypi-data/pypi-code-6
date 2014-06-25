'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''
from PySide import QtCore

VERSION_MAJOR = 0
VERSION_MINOR = 11
VERSION_PATCH = 0
VERSION_STRING = str(VERSION_MAJOR) + "." + str(VERSION_MINOR) + "." + str(VERSION_PATCH)
GPL_VERSION = '3'
APPLICATION_NAME = 'MAP Client'
ORGANISATION_NAME = 'Musculo Skeletal'
ORGANISATION_DOMAIN = 'musculoskeletal.org'

DEFAULT_PMR_IPADDRESS = 'http://teaching.physiomeproject.org'
DEFAULT_CONSUMER_PUBLIC_TOKEN = 'ghRsy25tpMnt36Aj7R_LsxUS'
DEFAULT_CONSUMER_SECRET_TOKEN = '41IgdRjQS1HsO_mq8VN2M2Dg'

# Credentials follows:
#
# Key    OP8AKmDIlH7OkHaPWNbnb-zf
# Secret    QQcKMnyCjjb7JNDHA-Lwdu7p
#
# The scope that should be used
#
# from urllib import quote_plus
# DEFAULT_SCOPE = quote_plus(
#     'http://localhost:8280/pmr/scope/collection,'
#     'http://localhost:8280/pmr/scope/search,'
#     'http://localhost:8280/pmr/scope/workspace_tempauth,'
#     'http://localhost:8280/pmr/scope/workspace_full'
# )

# Contributors list
HS = {'name': 'Hugh Sorby', 'email': 'h.sorby@auckland.ac.nz'}

CREDITS = {
           'programming'  : [HS],
           'artwork'      : [HS],
           'documentation': [HS]
           }

ABOUT = {
         'name'       : APPLICATION_NAME,
         'version'    : VERSION_STRING,
         'license'    : 'GNU GPL v.' + GPL_VERSION,
         'description': 'Create and manage detailed musculoskeletal models for OpenSim.'
         }

# APPLICATION
DEFAULT_WORKFLOW_PROJECT_FILENAME = '.workflow.conf'
DEFAULT_WORKFLOW_ANNOTATION_FILENAME = '.workflow.rdf'

class PMRInfo(object):

    def __init__(self):
        self.readSettings()

    def readSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('PMR')
        # pmr_host?  this is a domain name...
        self.ipaddress = settings.value('pmr-website', DEFAULT_PMR_IPADDRESS)
        self.host = self.ipaddress
        self.consumer_public_token = settings.value('consumer-public-token', DEFAULT_CONSUMER_PUBLIC_TOKEN)
        self.consumer_secret_token = settings.value('consumer-secret-token', DEFAULT_CONSUMER_SECRET_TOKEN)
        self.user_public_token = settings.value('user-public-token', None)
        self.user_secret_token = settings.value('user-secret-token', None)
        settings.endGroup()

    def writeSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('PMR')

        temp_public = self.user_public_token or ''
        temp_secret = self.user_secret_token or ''

        settings.setValue('user-public-token', temp_public)
        settings.setValue('user-secret-token', temp_secret)
        settings.endGroup()

    def update_token(self, oauth_token, oauth_token_secret):
        self.user_public_token = oauth_token
        self.user_secret_token = oauth_token_secret
        self.writeSettings()

    def has_access(self):
        return bool(self.user_public_token and self.user_secret_token)

    def get_session_kwargs(self):
        return {
            'client_key': self.consumer_public_token,
            'client_secret': self.consumer_secret_token,
            'resource_owner_key': self.user_public_token,
            'resource_owner_secret': self.user_secret_token,
        }
