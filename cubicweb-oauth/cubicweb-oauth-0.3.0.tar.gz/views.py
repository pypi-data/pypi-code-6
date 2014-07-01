# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-oauth views/forms/actions/components for web ui"""

import json
import re
import urllib
import urlparse
import unicodedata

from cubicweb.utils import make_uid
from cubicweb.predicates import (
    anonymous_user, configuration_values, match_form_params)

from cubicweb.view import View
from cubicweb.web.controller import Controller
from cubicweb.web.views import authentication
from cubicweb.web.views import basecomponents, basetemplates
from cubicweb.web import Redirect, formfields, formwidgets, LogOut

from cubicweb.web import InvalidSession

from cubicweb import NoResultError, MultipleResultsError

from cubes.oauth.authplugin import EXT_TOKEN

_ = unicode

# XXX replace with multi-instance safe mechanism
NEGOSTATE = {}  # negoid -> service coordinates
COLLECT_LIST = []

login_re = re.compile('(?P<base>.*)(\.(?P<index>\d+))?')


def get_next_login(login):
    m = login_re.match(login)
    assert m is not None
    if m.group('index'):
        index = int(m.group('index')) + 1
    else:
        index = 1
    return '{}.{}'.format(login, index)


class ExternalAuthMixin(object):
    def get_service(self, req, cnx, providername):
        try:
            return cnx.execute(
                'ExternalAuthService S WHERE S provider P, P spid %(spid)s',
                {'spid': providername}
            ).one()
        except (NoResultError, MultipleResultsError):
            self.exception('no service for provider: %s' % providername)
            raise Redirect(req.build_url(
                __message='no service for provider %s' % providername
            ))


class ExternalAuthUserInfos(Controller):
    __regid__ = 'externalauth-userinfos'

    def publish(self, rset=None):
        if self._cw.session.anonymous_session:
            ret = {'anonymous': True}
        else:
            ret = {
                'anonymous': False,
                'login': self._cw.user.login
            }
        return json.dumps(ret)


class ExternalAuthConfirm(Controller):
    __regid__ = 'externalauth-confirm'
    __select__ = match_form_params('code', '__externalauth_negociationid')

    def publish(self, rset=None):
        form = self._cw.form
        negociationid = form.get('__externalauth_negociationid')

        if not negociationid:
            raise Redirect(self._cw.build_url())

        nego = NEGOSTATE.pop(negociationid, None)

        if nego is None:
            raise Redirect(self._cw.build_url())

        # XXX If the user was created just now, optionnaly redirect to its
        # profile instead of the final_redirect
        raise Redirect(self._cw.build_url(nego['final_redirect']))


class ExternalAuthError(Controller):
    __regid__ = 'externalauth-confirm'
    __select__ = match_form_params(
        'code_error', 'code_message', '__externalauth_negociationid')

    def publish(self, rset=None):
        form = self._cw.form

        raise Redirect(self._cw.build_url(
            __message='error while authenticating: %s %s'
            % (form.get('error_code'), form.get('error_message', ''))))


class ExternalAuthRetrieverStart(
        ExternalAuthMixin, authentication.WebAuthInfoRetriever):
    """External authentication first step.

    Will only redirect on the demanded service.
    """
    __regid__ = 'externalauth-authenticate-start'
    order = 9

    def request_has_auth_info(self, req):
        return '__externalauthprovider' in req.form

    def revalidate_login(self, req):
        # Always invalidate the current session
        raise InvalidSession()

    def authentication_information(self, req):
        providername = req.form.get('__externalauthprovider')
        if providername is None:
            raise authentication.NoAuthInfo

        self.info(
            'external authenticator (%s) building auth info %s',
            self.__class__.__name__, req.form
        )

        vreg = self._cw  # YES, see cw/web/views/authentication.py ~106
        repo = vreg.config.repository(vreg)
        with repo.internal_cnx() as cnx:
            service = self.get_service(req, cnx, providername)
            path = req.relative_path(includeparams=True)
            # Remove the 'vid' parameter if the selected view is 'loggedout'
            if '?' in path:
                path, query = path.split('?', 1)
                params = urlparse.parse_qs(query)
                if params.get('vid') == ['loggedout']:
                    del params['vid']
                params.pop('__externalauthprovider', None)
                if params:
                    path = '?'.join(
                        (path, urllib.urlencode(params, doseq=True)))

            negoid = make_uid('nego')
            nego = {'service': service.eid,
                    'redirect_uri': req.build_url(
                        'externalauth-confirm',
                        __externalauth_negociationid=negoid
                    ),
                    'final_redirect': path}
            NEGOSTATE[negoid] = nego
            service_adapter = service.cw_adapt_to('externalauth.service')
            url = service_adapter.oauth2_service.get_authorize_url(
                redirect_uri=nego['redirect_uri'],
                scope=service_adapter.provider.scope
            )
            raise Redirect(url)


class ExternalAuthRetrieverMixin(ExternalAuthMixin):
    def _authentication_information(
            self, req, cnx, adapter, service, oauth2_session, autologin=False):
        try:
            infos = adapter.provider.retrieve_info(oauth2_session)
            extid_rset = cnx.execute(
                'ExternalIdentity SI WHERE SI provider P, '
                'P eid %(peid)s, SI uid %(uid)s',
                {'peid': service.provider[0].eid, 'uid': infos['uid']}
            )
            assert extid_rset.rowcount < 2
            if extid_rset:
                external_identity = extid_rset.get_entity(0, 0)
                if autologin and not external_identity.autologin:
                    self.info(
                        "Autologin is not enabled for identity %s",
                        infos['uid'])
                    raise authentication.NoAuthInfo
            else:
                external_identity = cnx.create_entity(
                    'ExternalIdentity', provider=service.provider[0],
                    uid=infos['uid']
                )

            # deactivate any previous access_token
            cnx.execute(
                'SET X active FALSE WHERE '
                'X is OAuth2Session, '
                'S external_identity SI, SI eid %(sieid)s, '
                'S service SE, SE eid %(seid)s',
                {'sieid': external_identity.eid, 'seid': service.eid}
            )
            oauth2_session = cnx.create_entity(
                'OAuth2Session', service=service,
                external_identity=external_identity,
                access_token=oauth2_session.access_token,
                active=True
            )

            cnx.commit(free_cnxset=False)
        except authentication.NoAuthInfo:
            raise
        except Exception, e:
            self.exception("Cannot get the oauth2_session")
            raise authentication.NoAuthInfo(str(e))

        if external_identity.identity_of:
            user = external_identity.identity_of[0]
            login = user.login
            external_identity.cw_set(autologin=True)
            cnx.commit()
            self.info('identified %s on %s as %s' % (
                user.login, service.provider[0].name, infos['uid']))
        else:
            self.debug(
                "Unknown identity %s on %s: will create a local account",
                infos['uid'], service.provider[0].name)

            login = self.forge_login(cnx, infos)
            password = make_uid()

            # TODO insert more informations from the external service
            # XXX We should loop around the call_service and retry with a
            # different login (w. get_next_login) when it raises a
            # ValidationError _or_ if the commit() raise a duplicate key
            # error.

            try:
                user = cnx.call_service(
                    'register_user',
                    login=login,
                    password=password,
                    email=infos.get('email', None),
                    firstname=infos.get('firstname', u''),
                    surname=infos.get('lastname', u''))

                cnx.execute(
                    'SET X identity_of U '
                    'WHERE X eid %(sieid)s, '
                    'U is CWUser, U login %(login)s',
                    {'sieid': external_identity.eid,
                     'login': login}
                )
                external_identity.cw_set(autologin=True)
                cnx.commit()
                self.info('created user %s on %s as %s' % (
                    user.login, service.provider[0].name, infos['uid']))
            except:
                self.exception("Cannot create user %s" % login)
                raise

        return login, {'__externalauth_directauth': EXT_TOKEN}


class ExternalAuthRetrieverDirect(
        ExternalAuthRetrieverMixin, authentication.WebAuthInfoRetriever):
    __regid__ = 'externalauth-direct'

    order = ExternalAuthRetrieverStart.order - 1

    def request_has_auth_info(self, req):
        return (
            '__externalauthprovider' in req.form
            and '__externalauth_oauth2_token' in req.form)

    def revalidate_login(self, req):
        # Always invalidate the current session
        raise InvalidSession()

    def authentication_information(self, req):
        if not self.request_has_auth_info(req):
            raise authentication.NoAuthInfo

        spid = req.form.get('__externalauthprovider')
        oauth2_token = req.form.get('__externalauth_oauth2_token')
        autologin = bool(req.form.get('autologin'))

        vreg = self._cw  # YES, see cw/web/views/authentication.py ~106
        repo = vreg.config.repository(vreg)
        with repo.internal_cnx() as cnx:
            try:
                service = self.get_service(req, cnx, spid)
                adapter = service.cw_adapt_to('externalauth.service')
                oauth2_session = adapter.oauth2_service.get_session(
                    oauth2_token)
            except:
                self.error("Cannot get a auth2session")
                raise authentication.NoAuthInfo
            return self._authentication_information(
                req, cnx, adapter, service, oauth2_session,
                autologin=autologin)


class ExternalAuthRetrieverFinish(
        ExternalAuthRetrieverMixin, authentication.WebAuthInfoRetriever):
    __regid__ = 'externalauth-success'
    order = ExternalAuthRetrieverStart.order - 1

    def request_has_auth_info(self, req):
        return (
            '__externalauth_negociationid' in req.form
            and 'code' in req.form)

    def revalidate_login(self, req):
        # Always invalidate the current session
        raise InvalidSession()

    def authentication_information(self, req):
        if not self.request_has_auth_info(req):
            raise authentication.NoAuthInfo

        self.info('external authenticator (%s) building auth info %s',
                  self.__class__.__name__, req.form)

        code = req.form.get('code')
        negociationid = req.form.get('__externalauth_negociationid')

        if not (code and negociationid):
            raise authentication.NoAuthInfo("Invalid oauth code/negociationid")

        nego = NEGOSTATE.get(negociationid, None)

        if nego is None:
            raise authentication.NoAuthInfo(req._('Authentication timeout.'))

        vreg = self._cw  # YES, see cw/web/views/authentication.py ~106
        repo = vreg.config.repository(vreg)
        with repo.internal_cnx() as cnx:
            try:
                service = cnx.entity_from_eid(nego['service'])
                adapter = service.cw_adapt_to('externalauth.service')
                oauth2_session = adapter.oauth2_service.get_auth_session(data={
                    'code': code,
                    'redirect_uri': nego['redirect_uri']
                })
            except:
                self.error("Cannot get a auth2session")
                raise authentication.NoAuthInfo
            return self._authentication_information(
                req, cnx, adapter, service, oauth2_session)

    def make_unique_login(self, cnx, login):
        """Return a login that does not yet exists in the database,
        based on the given login"""
        q = 'Any X WHERE X is CWUser, X login %(login)s'
        while True:
            rset = cnx.execute(q, {'login': login})
            if not rset.rowcount:
                break
            login = get_next_login(login)
        return login

    def normalize_login(self, login):
        """Return a string suitable to be a login, based on the given login"""
        login = unicodedata.normalize('NFKD', login)
        login = login.encode('ascii', 'ignore')
        login = login.replace(' ', '.').lower()
        return unicode(login)

    def forge_login(self, cnx, infos):
        """Forge a login based on infos comming from the oauth2 provider.
        """
        if infos.get('name'):
            login = infos['name']
        elif infos.get('firstname') or infos.get('lastname'):
            login = u'{}.{}'.format(
                infos.get('firstname') or u'',
                infos.get('lastname') or u'').strip('.')
        elif infos.get('username'):
            login = infos.get('username')
        elif infos.get('email'):
            login = infos['email'].split('@', 1)[0]
        else:
            login = infos['uid']

        login = self.normalize_login(login)

        return self.make_unique_login(cnx, login)


# form, link and view

class ExternalAuthLogForm(basetemplates.BaseLogForm):
    __regid__ = domid = 'externalauthlogform'
    boxid = 'externalauthlogbox'

    action = ''

    __externalauthprovider = formfields.StringField(
        '__externalauthprovider', label=_('externalauthprovider'),
        widget=formwidgets.TextInput({'class': 'data'}),
        # NOTE: could be a dropdown with a pre-cooked list ...
        value='facebook'
    )

    onclick_args = ('externalauthlogbox', '__externalauthprovider')


class ExternalAuthLoginLink(ExternalAuthMixin, basecomponents.HeaderComponent):
    __regid__ = 'externalauthlink'
    __select__ = (
        basecomponents.HeaderComponent.__select__ and
        configuration_values('auth-mode', 'cookie') &
        anonymous_user()
    )

    context = _('header-right')
    onclick = "javascript: cw.htmlhelpers.popupLoginBox('%s', '%s');"

    def autologin_script(self):
        with self._cw.cnx._repo.internal_cnx() as cnx:
            for spid in ('facebook',):
                self._cw.html_headers.add_post_inline_script(
                    self.get_service(self._cw, cnx, spid).cw_adapt_to(
                        'externalauth.service'
                    ).autologin_script()
                )

    def render(self, w):
        text = self._cw._('external auth login')
        w(u"""<a href="#" onclick="%s">%s</a>""" % (
            self.onclick % ('externalauthlogbox', '__externalauthprovider'),
            text
        ))
        self._cw.view(
            'externalauthlogform', rset=self.cw_rset,
            id='externalauthlogbox', w=w
        )
        self.autologin_script()


class ExternalAuthLogFormView(View):
    __regid__ = 'externalauthlogform'
    __select__ = configuration_values('auth-mode', 'cookie')

    help_msg = _("""
Select the provider you want to use to authenticate.
    """)

    title = _('log in using a provider')

    def call(self, id='externalauthlogbox'):
        w = self.w

        w(u'<div id="%s" class="popupLoginBox hidden">' % id)
        w(u'<p>%s</p>' % self._cw._(self.help_msg))
        form = self._cw.vreg['forms'].select('externalauthlogform', self._cw)
        form.render(w=w)
        w(u'</div>')


# XXX Hijack the logout method.
# We should have a hook for pre/post-logout actions
def CookieSessionHandler_logout(self, req, goto_url):
    if req.user.reverse_identity_of:
        req.user.reverse_identity_of[0].cw_set(autologin=False)
        req.cnx.commit()
    self.session_manager.close_session(req.session)
    req.remove_cookie(self.session_cookie(req))
    raise LogOut(url=goto_url)

from cubicweb.web.application import CookieSessionHandler
CookieSessionHandler.logout = CookieSessionHandler_logout
