# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node, Arc


class MainUser(Node):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    groups = ndb.StringProperty(repeated=True)

    @classmethod
    def query_email_starts_with(cls, prefix=''):
        last_str_with_prefix = prefix + unichr(0x110000 - 1)
        return cls.query(cls.email >= prefix, cls.email < last_str_with_prefix).order(cls.email)

    @classmethod
    def query_email(cls, email):
        return cls.query(cls.email == email)


# Users from external providers

class ExternalUser(Node):
    external_id = ndb.StringProperty(required=True)

    @classmethod
    def query_by_external_id(cls, external_id):
        return cls.query(cls.external_id == external_id)


class ExternalToMainUser(Arc):
    destination = ndb.KeyProperty(MainUser, required=True)
    origin = ndb.KeyProperty(ExternalUser, required=True)


class PendingExternalToMainUser(Node):
    """
    Class used to create ExternalToMainUser after email confirmation
    """
    main_user = ndb.KeyProperty(MainUser, required=True, indexed=False)
    external_user = ndb.KeyProperty(required=True, indexed=False)
    # name = ndb.StringProperty(required=True, indexed=False)
    # email = ndb.StringProperty(required=True, indexed=False)


class GoogleUser(ExternalUser):
    pass


class PasswordlessUser(ExternalUser):
    pass


class FacebookUser(ExternalUser):
    pass




