import datetime as dt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound 
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.types import DateTime
from flask import flash, url_for, redirect, session
from wtforms.fields import StringField, HiddenField, SubmitField
from wtforms.validators import InputRequired
from openid.store import nonce
from openid.store.interface import OpenIDStore
from openid.association import Association
from openid.consumer import consumer
from openid.consumer.discover import DiscoveryFailure
from openid.extensions import sreg
from openid.yadis.constants import YADIS_HEADER_NAME, YADIS_CONTENT_TYPE

from .. import db, auth_methods, requests_session
from . import AuthMethod, AuthForm
from .models import User, Group


class OpenIDForm(AuthForm):
    url = StringField('Identifier', validators=[InputRequired()])
    submit = SubmitField('Login')


class OpenID(AuthMethod):
    name = "OpenID"

    def __init__(self, **kwargs):
        self.store = SRPOpenIDStore()

    def form(self):
        return OpenIDForm.append_field('auth_method',
                HiddenField(default=self.name))

    def login(self, form):
        con = consumer.Consumer(session, self.store)
        try:
            auth_request = con.begin(form.url.data)
        except DiscoveryFailure:
            flash("OpenID discovery error: {}".format(e), 'error')
            redirect(url_for('login'))
        else:
            # Get a nickname to identify the user with
            sreg_request = sreg.SRegRequest(required=['nickname'])
            auth_request.addExtension(sreg_request)
            # set up redirect URLs
            start_url = url_for('login')
            end_url = url_for('login',
                    auth_method=self.__class__.__name__.lower())
            auth_url = auth_request.redirectURL(start_url, end_url)
            return redirect(auth_url)

    def view(self):
        if request.method == 'POST':
            args = request.form
        elif request.method == 'GET':
            args = request.args
        if args:
            # Check OpenID response
            con = consumer.Consumer(session, self.store)
            end_url = url_for('login',
                    auth_method=self.__class__.__name__.lower())
            response = con.complete(args, end_url)
            # Check the response for the requested info
            sreg_response = {}
            if response.status == consumer.SUCCESS:
                sreg_response = sreg.SRegResponse.fromSuccessResponse(response)
                user = OpenIDUser()
                user.nickname = sreg_response['nickname']
                print(user.nickname)
                db.session.add(user)
                db.session.commit()
            else:
                flash("Error logging in with OpenID", 'error')


class SRPOpenIDStore(OpenIDStore):
    def storeAssociation(self, url, association):
        oid_user = OpenIDUser(url, association)
        db.session.add(oid_user)
        db.session.commit()

    def getAssociation(self, server_url, handle=None):
        assoc_query = OpenIDAssociation.query.filter_by(url=server_url)
        if handle is not None:
            assoc_query = assoc_query.filter_by(handle=handle)
        assoc_query = assoc_query.order_by(OpenIDAssociation.issued.desc())
        association = assoc_query.first()
        if assoc_query.expired:
            return None
        else:
            return association

    def removeAssociation(self, server_url, handle):
        query = OpenIDAssociation.query.filter_by(url=server_url, handle=handle)
        if query.exists():
            query.delete()
            db.session.commit()
            return True
        else:
            return False

    def useNonce(self, server_url, timestamp, salt):
        dt_stamp = dt.datetime.utcfromtimestamp(timestamp)
        nonce = OpenIDNonce(server_url, dt_stamp, salt)
        if nonce.valid(nonce.SKEW):
            return False
        try:
            db.session.add(nonce)
            db.session.commit()
        except IntegrityError:
            return False
        else:
            return True

    def cleanupNonces(self):
        skew = dt.timedelta(nonce.SKEW)
        return OpenIDNonce.query.filter(OpenIDNonce.valid(skew).delete())

    def cleanupAssociations(self):
        return OpenIDAssociation.query.filter(OpenIDAssociation.expired).\
                delete()


class OpenIDNonce(db.Model):
    __tablename__ = 'openidnonce'
    url = db.Column(db.String(2000), primary_key=True)
    timestamp = db.Column(DateTime(), primary_key=True)
    salt = db.Column(db.String(40), primary_key=40)

    def __init__(self, url, timestamp, salt):
        self.url = url
        self.timestamp = timestamp
        self.salt = salt

    @hybrid_method
    def valid(self, skew):
        return (self.timestamp - dt.datetime.utcnow()) <= dt.timedelta(skew)


class OpenIDAssociation(db.Model):
    __tablename__ = 'openidassociation'
    handle = db.Column(db.String(100), primary_key=True)
    url = db.Column(db.String(2000), primary_key=True)
    secret = db.Column(db.LargeBinary(128), nullable=False)
    issued = db.Column(db.DateTime(), nullable=False)
    lifetime = db.Column(db.Interval(), nullable=False)
    type_ = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('openiduser.id'))

    def __init__(self, url, association):
        self.url = url
        self.handle = association.handle
        if isinstance(association.secret):
            self.secret = association.secret.encode('utf-8')
        else:
            self.secret = association.secret
        self.issued = dt.datetime.utcfromtimestamp(association.issued)
        self.lifetime = dt.timedelta(association.lifetime)
        self.type_ = association.assoc_type

    @hybrid_property
    def expired(self):
        return (self.issued + self.interval) < dt.datetime.utcnow()


class OpenIDUser(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    nickname = db.Column(db.String(200), nullable=False)
    associations = db.relationship('OpenIDAssociation', collection_class=list,
            back_populates='user', order_by=OpenIDAssociation.issued.desc())

    @classmethod
    def authmethod(cls):
        return OpenID
