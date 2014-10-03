# -*- coding: utf-8 -*-
from laas_client import LaaSClient
import logging


LOG = logging.getLogger(__name__)

class LaaSProvider(object):

    @classmethod
    def get_credentials(self, environment):
        LOG.info("Getting credentials...")
        from dbaas_credentials.credential import Credential
        from dbaas_credentials.models import CredentialType
        integration = CredentialType.objects.get(type= CredentialType.LAAS)

        return Credential.get_credentials(environment= environment, integration= integration)

    @classmethod
    def auth(self, environment):
        LOG.info("Conecting with laas...")
        credentials = self.get_credentials(environment= environment)
        self.project_url = credentials.project
        self.team_url = credentials.team
        return LaaSClient(base_url= credentials.endpoint, username=credentials.user, password= credentials.password)

    @classmethod
    def update_laas_workspace(self, environment, laas_workspace):
        laas = self.auth(environment=environment)
        laas.update_data(http_verb="POST", endpoint=self.project_url, payload=laas_workspace)

    @classmethod
    def update_laas_team(self, environment, laas_team):
        laas = self.auth(environment=environment)
        laas.update_data(http_verb="PUT", endpoint=self.team_url, payload=laas_team)
