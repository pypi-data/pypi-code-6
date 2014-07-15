from squirro.common.dependency import register, register_instance, \
    get_injected
from squirro.common.context import create_short_uuid
from squirro.lib.user.model import Base as BaseUser, Client, Tenant, User, \
    AccessToken, UserSession, Authentication
from squirro.lib.topic.model import Base as BaseTopic
from squirro.api.bulk.model import Base as BaseBulk
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime, timedelta


class DummyIndexReader(object):
    """Class which can be used as a dummy index reader."""

    def __init__(self, items):
        self.items = items
        self.kwargs = None

    def read_items_by(self, **kwargs):
        self.kwargs = kwargs
        return {'items': self.items, 'total': len(self.items)}

    def read_item(self, *args, **kwargs):
        item_id = args[0]
        for i in self.items:
            if i['id'] == item_id:
                return i
        return None

    def get_refids_of(self, *args, **kwargs):
        return ()


class DummyFingerprintClient(object):
    """Class to be used as a dummy fingerprint client."""
    def __init__(self, raise_exception=None):
        self.raise_exception = raise_exception

    def recalculate_fingerprint_selected_features(self, type, type_id):
        if self.raise_exception:
            raise self.raise_exception


def setup_session():
    """Method to setup a memory database session for the provided
    `unittest.TestCase` instance.
    """

    engine = create_engine('sqlite:///:memory:', echo=True)

    BaseUser.metadata.create_all(engine)
    BaseTopic.metadata.create_all(engine)
    BaseBulk.metadata.create_all(engine)
    Session = scoped_session(sessionmaker(engine))
    register('session', Session)
    register_instance('session_cls', Session)

    register('utcnow', datetime.utcnow)
    register('short_uuid', create_short_uuid)


def setup_session_user_objects():
    """Method to create the necessary database objects such that we can use
    the user API.
    """

    session = get_injected('session')

    # client
    client = Client(id='client01', client_secret='secret01', trusted=True)
    session.add(client)

    # tenant
    tenant = Tenant(id='tenant01', domain='tenant01')
    session.add(tenant)

    # user
    user = User(id='user01', tenant_id=tenant.id, email='me@squirro.com',
                role='admin')
    user.set_password('test')
    session.add(user)

    # user session
    valid_to = get_injected('utcnow') + timedelta(hours=10)
    user_session = UserSession(
        id='session01', client_id=client.id, refresh_token='token02',
        user_id=user.id, refresh_valid_to=valid_to)
    session.add(user_session)

    # access token
    valid_to = get_injected('utcnow') + timedelta(hours=1)
    token = AccessToken(
        id='token01', session_id=user_session.id, valid_to=valid_to)
    session.add(token)

    # authentication
    auth = Authentication(
        id='auth01', user_id=user.id, service='salesforce',
        service_user='sfdc01', client_id=client.id)
    session.add(auth)

    # commit
    session.commit()


class DummyUserProxy(object):
    """Simulate a admin user with all permissions."""

    def get_permissions(self, tenant, user_id, project_id):
        return ['*']

    def get_user_memberships(self, user_id):
        return {
            'memberships': [],
            'server_role': 'admin',
            'admin_membership': {
                'project_role': 'admin',
                'permissions': ['*'],
            },
        }

    def set_membership(self, tenant, user_id, project_id, role):
        return ['*']

    def delete_membership(self, tenant, user_id, project_id):
        pass
