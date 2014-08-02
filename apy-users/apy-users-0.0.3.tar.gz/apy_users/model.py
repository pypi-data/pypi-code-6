from os import urandom
from binascii import hexlify
from time import time
from .entities import Account, AccountRepository
from abc import abstractmethod, ABCMeta
from email.mime.text import MIMEText


class UsernameAlreadyInUseException(Exception):
    pass


class EmailAlreadyInUseException(Exception):
    pass


class WrongPasswordException(Exception):
    pass


class WrongConsumerAccessTokenException(Exception):
    pass


class UserBannedException(Exception):
    pass


class ExpiredConsumerException(Exception):
    pass


class UserNotBannedException(Exception):
    pass


class UserCurrentlyBannedException(Exception):
    pass


class EmailNotConfirmedException(Exception):
    pass


class EmailCurrentlyConfirmedException(Exception):
    pass


class SignUp:
    def __init__(self, account_repository, consumer_manager, email_confirmation_sender):
        """
        @type account_repository AccountRepository
        @type consumer_manager ConsumerManager
        @type email_confirmation_sender user_apy_addon.model.EmailConfirmationSender
        """
        self._account_repository = account_repository
        self._consumer_manager = consumer_manager
        self._email_confirmation_sender = email_confirmation_sender

    def create_account(self, username, email, password):
        """
        @type username str
        @type email str
        @type password str
        """
        self._validate_account_data(username, email)

        account = Account(
            client_id=hexlify(urandom(16)),
            username=username,
            email=email,
            password=password,
            consumers=[],
            is_email_confirmed=False,
            is_banned=False,
            creation_ts=int(time()),
            last_authentication_ts=False
        )
        consumer = account.create_consumer(tags=['email_confirmation'])

        self._email_confirmation_sender.send(email, consumer.access_token)

        return self._account_repository.add(account)

    def confirm_email(self, consumer_access_token):
        account = self._account_repository.find_by_consumer_access_token(consumer_access_token)

        if account is None:
            raise WrongConsumerAccessTokenException()

        if account.is_email_confirmed:
            raise EmailCurrentlyConfirmedException()

        account.is_email_confirmed = True
        account.remove_consumer_by_access_token(consumer_access_token)
        return self._account_repository.update(account)

    def _validate_account_data(self, username, email):
        if self._is_username_occupied(username):
            raise UsernameAlreadyInUseException()
        if self._is_email_occupied(email):
            raise EmailAlreadyInUseException()

    def _is_username_occupied(self, username):
        """ @type username str """
        return self._account_repository.find_by_username(username) is not None

    def _is_email_occupied(self, email):
        """ @type email str """
        return self._account_repository.find_by_email(email) is not None


class AccountModerator:
    def __init__(self, account_repository):
        self._account_repository = account_repository

    def ban(self, account):
        if account.is_banned is True:
            raise UserCurrentlyBannedException

        account.is_banned = True
        self._account_repository.update(account)

    @staticmethod
    def is_banned(account):
        return account.is_banned

    def unban(self, account):
        if account.is_banned is False:
            raise UserNotBannedException

        account.is_banned = False
        self._account_repository.update(account)


class AccountEditor:
    def __init__(self, account_repository):
        self._account_repository = account_repository

    def change_password(self, account, new_password):
        account.password = new_password
        self._account_repository.update(account)

    def change_email(self, account, email):
        if self._account_repository.find_by_email(email) is not None:
            raise EmailAlreadyInUseException()

        account.email = email
        account.is_email_confirmed = False
        self._account_repository.update(account)

    def change_username(self, account, username):
        if self._account_repository.find_by_username(username) is not None:
            raise UsernameAlreadyInUseException()

        account.username = username
        self._account_repository.update(account)


class ConsumerManager:
    def __init__(self, account_repository, authenticator):
        self._account_repository = account_repository
        self._authenticator = authenticator

    def create_web_consumer(self, username, password):
        account = self._account_repository.find_by_username(username)

        self._authenticator.validate_password(account, password)

        consumer = account.create_consumer(tags=['web'])
        self._account_repository.update(account)
        return consumer.access_token


class Authenticator:
    def __init__(self, account_repository, check_if_email_is_confirmed=True, delete_expired_consumers=True):
        """
        @type account_repository AccountRepository
        @type check_if_email_is_confirmed bool
        """
        self._account_repository = account_repository
        self._check_if_email_is_confirmed = check_if_email_is_confirmed
        self._delete_expired_consumers = delete_expired_consumers

    def validate_password(self, account, password, ignore_email_confirmation=False):
        if account.password != password:
            raise WrongPasswordException()
        if account.is_banned:
            raise UserBannedException()
        if not ignore_email_confirmation and self._check_if_email_is_confirmed and not account.is_email_confirmed:
            raise EmailNotConfirmedException()
        account.last_authentication_ts = int(time())
        self._account_repository.update(account)

    def validate_consumer_access_token(self, account, consumer_access_token, ignore_email_confirmation=False):
        consumer = account.find_consumer_by_access_token(consumer_access_token)

        if consumer is None:
            raise WrongConsumerAccessTokenException()

        if consumer.is_expired():
            if self._delete_expired_consumers:
                account.remove_consumer_by_access_token(consumer_access_token)
                self._account_repository.update(account)
            raise ExpiredConsumerException()

        if account.is_banned:
            raise UserBannedException()

        if not ignore_email_confirmation and self._check_if_email_is_confirmed and not account.is_email_confirmed:
            raise EmailNotConfirmedException()

        account.last_authentication_ts = int(time())
        self._account_repository.update(account)


class EmailConfirmationSender:
    __metaclass__ = ABCMeta

    @abstractmethod
    def send(self, email, access_token):
        """
        @type email str
        @type access_token str
        """

class MailTransfer:
    def __init__(self, smtp):
        self._smtp = smtp

    def send(self, from_, to, subject, content):
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = from_
        msg['To'] = to
        result = self._smtp.sendmail(from_, to, msg.as_string())
        self._smtp.quit()
        return result


class ExampleEmailConfirmationSender:
    def __init__(self, smtp, from_, base_url, subject):
        self._smtp = smtp
        self._from = from_
        self._base_url = base_url
        self._subject = subject

    def send(self, email, access_token):
        content = '%s/%s' % (self._base_url, access_token)
        return self._smtp.send(self._from, email, self._subject, content)

