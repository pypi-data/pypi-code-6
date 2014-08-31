"""
Profiles model reference implementation.
"""

from time import time as timestamp

import logging
logger = logging.getLogger('fanery.admin')


class Profile:

    @classmethod
    def initialize(cls, record):
        from _state import get_state
        record.merge(domain=get_state().domain)

    @classmethod
    def validate(cls, record):
        from _term import is_str, is_email, Hict

        errors, dct = Hict(), record._dct

        domain = dct.get('domain')
        if not domain:
            errors.domain.required = domain

        username = dct.get('username')
        if not username:
            errors.username.required = username
        elif not is_str(username):
            errors.username.bad_type = type(username).__name__

        password_hash = dct.get('password_hash')
        if not password_hash:
            errors.password.required = password_hash

        email = dct.get('email')
        if not email:
            errors.email.required = email
        elif not is_str(email):
            errors.email.bad_type = type(email).__name__
        elif not is_email(email):
            errors.email.bad_format = email

        if errors:
            print dct
        return errors

    @classmethod
    def index(cls, record):
        return dict((k, v) for k, v in record._dct.iteritems()
                    if not k.startswith('password_'))


def setup(db):
    from _store import add_model, add_storage

    start = timestamp()
    try:
        add_model(Profile)
        add_storage(db, Profile)
    finally:
        logger.debug('%0.6f setup' % (timestamp() - start))


def init(admin_username='admin', admin_password=None, **extra):
    from _crypto import nacl_random
    from _state import get_state
    from _store import storage
    from _term import is_str
    from _auth import hooks
    from scrypt import hash

    start = timestamp()
    try:
        state = get_state()
        domain = state.domain = extra.setdefault('domain', state.domain)
        extra.setdefault('email', '%s@%s' % (admin_username, 'example.com'))

        admin = hooks.fetch_profile(domain, admin_username)
        if admin is None:
            if not admin_password:
                admin_password = nacl_random(16).encode('hex')
            else:
                assert is_str(admin_password), 'bad-type'

            salt = nacl_random(16)
            password_hash = hash(admin_password, salt)

            desc = "adduser %s:%s@%s" % (admin_username, admin_password, domain)    # noqa
            with storage(desc) as db:
                db.insert(Profile,
                          username=admin_username,
                          password_hash=password_hash,
                          password_salt=salt,
                          **extra)
    finally:
        logger.debug('%0.6f init' % (timestamp() - start))
