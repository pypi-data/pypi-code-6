import urllib
import urlparse
import mock

from cubicweb.devtools.httptest import CubicWebServerTC
from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.predicates import yes

from cubes.oauth.entities import ServiceAdapter
from cubes.oauth import views as oauth_views


class FakeRequestRession(object):
    return_value = None

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, url):
        if url.startswith('me?'):
            if self.return_value:
                m = self.return_value
                self.return_value = None
                return m
            m = mock.Mock()
            m.json.return_value = {
                'id': u'1111',
                'last_name': u'AName',
                'first_name': u'AFName',
                'username': u'zeuser',
                'email': u'zeuser@example.com'}
            return m
        return ''


class FakeRauthService(object):
    tokens = (u'token{}'.format(i) for i in xrange(9999))

    def __init__(
            self, name, client_id, client_secret, authorize_url,
            access_token_url, base_url):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorize_url = authorize_url
        self.access_token_url = access_token_url
        self.base_url = base_url

    def get_authorize_url(self, redirect_uri, scope):
        return self.authorize_url + '?' + urllib.urlencode(
            {"redirect_uri": redirect_uri, 'scope': scope})

    def get_auth_session(self, data):
        if data['code'] == u'goodcode':
            s = FakeRequestRession(self.base_url)
            s.access_token = self.tokens.next()
        return s


class FakeServiceAdapter(ServiceAdapter):
    __select__ = ServiceAdapter.__select__ & yes()

    @property
    def oauth2_service(self):
        provider = self.provider
        return FakeRauthService(
            name=self.entity.application_name,
            client_id=self.entity.application_id,
            client_secret=self.entity.application_secret,
            authorize_url=provider.authorize_url,
            access_token_url=provider.access_token_url,
            base_url=provider.base_url,
        )


class OAuthTC(CubicWebServerTC):
    anonymous_allowed = True

    application_name = u'oauth_test'
    application_id = u'123456'
    application_secret = u'secret'

    def setUp(self):
        CubicWebTC.setUp(self)
        self.vreg.register(FakeServiceAdapter)
        with self.admin_access.repo_cnx() as cnx:
            service = cnx.create_entity(
                'ExternalAuthService',
                provider=cnx.find(
                    'ExternalAuthProvider', spid='facebook').one(),
                application_name=self.application_name,
                application_id=self.application_id,
                application_secret=self.application_secret
                )
            self.provider = \
                service.cw_adapt_to('externalauth.service').provider
            cnx.commit()
        oauth_views.NEGOSTATE = {}
        self.start_server()

    def tearDown(self):
        self.vreg.unregister(FakeServiceAdapter)
        super(OAuthTC, self).tearDown()

    def login(self):
        response = self.web_request('?__externalauthprovider=facebook')
        location = response.getheader('location')

        redirect_uri = urlparse.parse_qs(
            location.split('?')[1])['redirect_uri'][0]
        assert redirect_uri.startswith(self.config['base-url'])

        url = redirect_uri + '&code=goodcode'
        url = url[len(self.config['base-url']):]

        return self.web_request(url)

    def test_wrong_providername(self):
        response = self.web_request('/?__externalauthprovider=wrong')
        self.assertEqual(303, response.status)

    def test_1st_redirect(self):
        response = self.web_request('/?__externalauthprovider=facebook')
        location = response.getheader('location')
        expected_location = self.provider.authorize_url + '?' \
            + urllib.urlencode({
                'scope': self.provider.scope,
                'redirect_uri':
                self.config.get('base-url') + 'externalauth-confirm'
                + '?__externalauth_negociationid='
                + oauth_views.NEGOSTATE.keys()[0]})
        self.assertEqual(
            expected_location, location)
        self.assertEqual(303, response.status)

    def test_creation(self):
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute('Any X WHERE X login "afname.aname"')
            self.assertEqual(0, rset.rowcount)

        response = self.login()
        location = response.getheader('location')
        expected_location = self.config['base-url']
        self.assertEqual(303, response.status)
        self.assertEqual(
            expected_location, location)

        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute('Any X WHERE X login "afname.aname"')
            self.assertEqual(1, rset.rowcount)

    def test_various_creation(self):
        def set_next_me(me):
            FakeRequestRession.return_value = mock.Mock()
            FakeRequestRession.return_value.json.return_value = me

        # with a name
        set_next_me({
            'id': u'1112',
            'name': u'Achille Zavata',
            'last_name': u'AName',
            'first_name': u'AFName',
            'username': u'zeuser',
            'email': u'zeuser@example.com'})

        self.login()
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute('Any X WHERE X login "achille.zavata"')
            self.assertEqual(1, rset.rowcount)

        # with only a first name
        set_next_me({
            'id': u'1113',
            'first_name': u'AFName',
            'last_name': u'',
            'username': u'zeuser',
            'email': u'zeuser2@example.com'})

        self.login()
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute('Any X WHERE X login "afname"')
            self.assertEqual(1, rset.rowcount)

        # with only a last name
        set_next_me({
            'id': u'1114',
            'last_name': u'AName',
            'username': u'zeuser',
            'email': u'zeuser3@example.com'})

        self.login()
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute('Any X WHERE X login "aname"')
            self.assertEqual(1, rset.rowcount)

        # with no name at all
        set_next_me({
            'id': u'1115',
            'name': u'',
            'last_name': None,
            'username': u'zeuser',
            'email': u'zeuser4@example.com'})

        self.login()
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute('Any X WHERE X login "zeuser"')
            self.assertEqual(1, rset.rowcount)

        # with no name nor username
        set_next_me({
            'id': u'1116',
            'name': u'',
            'last_name': None,
            'username': u'',
            'email': u'zeuser5@example.com'})

        self.login()
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute('Any X WHERE X login "zeuser5"')
            self.assertEqual(1, rset.rowcount)

        # with nothing but an id
        set_next_me({
            'id': u'1117'})

        self.login()
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute('Any X WHERE X login "1117"')
            self.assertEqual(1, rset.rowcount)

    def test_login(self):
        with self.admin_access.repo_cnx() as cnx:
            user = cnx.create_entity(
                'CWUser', login=u"zeuser", upassword='',
                in_group=cnx.find('CWGroup', name='users').one())
            cnx.create_entity(
                'ExternalIdentity',
                identity_of=user, provider=cnx.find(
                    'ExternalAuthProvider', spid='facebook').one(),
                uid=u'1111')
            rset = cnx.execute('Any X WHERE X login "zeuser"')
            self.assertEqual(1, rset.rowcount)
            cnx.commit()

        response = self.login()
        location = response.getheader('location')
        expected_location = self.config['base-url']
        self.assertEqual(303, response.status)
        self.assertEqual(expected_location, location)

        cookie = dict(
            token.strip().split('=') for token in
            response.getheader('Set-Cookie').split(';'))
        assert cookie['__data_session'].startswith("zeuser")

        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute('Any X WHERE X login "zeuser"')
            self.assertEqual(1, rset.rowcount)
