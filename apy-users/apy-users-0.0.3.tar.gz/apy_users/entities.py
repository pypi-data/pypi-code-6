from abc import abstractmethod, ABCMeta
from time import time
from copy import deepcopy
from os import urandom
from binascii import hexlify


class Account:
    def __init__(
            self,
            client_id,
            username,
            email,
            password,
            consumers,
            is_email_confirmed,
            is_banned,
            creation_ts,
            last_authentication_ts
    ):
        """
        @type client_id str
        @type username str
        @type email str
        @type password str
        @type consumers list of Consumer
        @type is_email_confirmed bool
        @type is_banned bool
        @type creation_ts int
        @type last_authentication_ts int or False
        """
        self.client_id = client_id
        self.username = username
        self.email = email
        self.password = password
        self.consumers = consumers
        self.is_email_confirmed = is_email_confirmed
        self.is_banned = is_banned
        self.creation_ts = creation_ts
        self.last_authentication_ts = last_authentication_ts

    def find_consumer_by_access_token(self, access_token):
        for consumer in self.consumers:
            if consumer.access_token == access_token:
                return consumer

        return None

    def create_consumer(self, description='', tags=None, seconds_to_expire=False, scopes=None):
        consumer = Consumer(
            description=description,
            tags=tags if tags is not None else [],
            access_token=hexlify(urandom(16)),
            creation_ts=int(time()),
            seconds_to_expire=seconds_to_expire,
            scopes=scopes if scopes is not None else []
        )
        self.consumers.append(consumer)
        return consumer

    def remove_consumer_by_access_token(self, access_token):
        consumers = []
        for consumer in self.consumers:
            if consumer.access_token != access_token:
                consumers.append(consumers)
        self.consumers = consumers


class Consumer:
    def __init__(
        self,
        description,
        tags,
        access_token,
        creation_ts,
        seconds_to_expire,
        scopes
    ):
        self.description = description
        self.tags = tags
        self.access_token = access_token
        self.creation_ts = creation_ts
        self.seconds_to_expire = seconds_to_expire
        self.scopes = scopes

    def is_expired(self):
        return self.seconds_to_expire is not False and int(time()) >= self.creation_ts + self.seconds_to_expire


class AccountRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def find_by_email(self, email):
        """
        @type email str
        @rtype: Account or None
        """

    @abstractmethod
    def find_by_username(self, username):
        """
        @type username str
        @rtype: Account or None
        """

    @abstractmethod
    def find_by_client_id(self, client_id):
        """
        @type client_id str
        @rtype: Account or None
        """

    @abstractmethod
    def find_by_consumer_access_token(self, consumer_access_token):
        """
        @type consumer_access_token str
        @rtype: Account or None
        """

    @abstractmethod
    def add(self, account):
        """
        @type account Account
        @rtype: bool
        """

    @abstractmethod
    def update(self, account):
        """
        @type account Account
        @rtype: bool
        """

    @staticmethod
    def _plain_account(account):
        account = deepcopy(account)
        consumers_data = []

        for consumer in account.consumers:
            consumers_data.append(consumer.__dict__)

        account.consumers = consumers_data
        return account.__dict__
