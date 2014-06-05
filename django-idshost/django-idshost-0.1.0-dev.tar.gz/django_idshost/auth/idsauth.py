from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth.backends import RemoteUserBackend, ModelBackend


class IdsRemoteUserBackend(RemoteUserBackend):

    def clean_username(self, username):
        return username[2:]


class IdsHeaderMiddleware(RemoteUserMiddleware):
    header = 'HTTP_IDS_USER'
