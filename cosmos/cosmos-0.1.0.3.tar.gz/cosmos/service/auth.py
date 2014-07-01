from cosmos.dataservice.objectservice import ObjectService
from cosmos.rbac.object import AccessType, COSMOS_USERS_OBJECT_NAME, SYSTEM_USER
import settings

__author__ = 'Maruf Maniruzzaman'

import tornado.web
from tornado import gen
from cosmos.service.requesthandler import *
import json
from cosmos.service.utils import MongoObjectJSONEncoder

PASSWORD_HMAC_SIGNATURE = "hmac:"
PASSWORD_COLUMN_NAME = "password"
USER_COOKIE_NAME = "user"

class LogoutHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        self.clear_cookie("user")
        self.redirect('/')


class LoginHandler(RequestHandler):
    @gen.coroutine
    def get(self):

        if self.current_user:
            self.redirect('/')

        self.render('login.html', user=None)

    @tornado.web.asynchronous
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        if not username or len(username)<1:
            data = json.loads(self.request.body)
            assert isinstance(data, dict)
            username = data.get("username")
            password = data.get("password")

        db = self.settings['db']
        object_name = COSMOS_USERS_OBJECT_NAME
        obj_serv = ObjectService()

        columns = ["username", "password", "roles"]
        query = {"username": username}

        obj_serv.find(SYSTEM_USER, db, object_name, query, columns, self._on_load_response)

    def _on_load_response(self, result, error):
        if error:
            raise tornado.web.HTTPError(500, error)
        else:
            assert isinstance(result, list)
            if not result or result.__len__() != 1:
                raise tornado.web.HTTPError(401, "Unauthorized")

            password = self.get_argument("password")
            if not password or len(password)<1:
                data = json.loads(self.request.body)
                assert isinstance(data, dict)
                password = data.get("password")

            user = result[0]
            loaded_password_hash = user.get(PASSWORD_COLUMN_NAME)
            validate_password(password, loaded_password_hash)
            del user["password"]
            self.set_secure_cookie(USER_COOKIE_NAME, MongoObjectJSONEncoder().encode(user))

            self.redirect('/')

def validate_password(password, saved_password_hash):
    hmac_password = get_hmac_password(password)
    try:
        #FIXME: WARNING possible attack: use hmac.compare_digest(a, b) instead (https://docs.python.org/2/library/hmac.html)
        if not saved_password_hash == hmac_password:
            raise tornado.web.HTTPError(401, "Unauthorized")
    except:
        raise tornado.web.HTTPError(401, "Unauthorized")


def get_hmac_password(password):
    hmac_hex = hmac.new(settings.HMAC_KEY, password).hexdigest()
    hmac_password = "{0}{1}".format(PASSWORD_HMAC_SIGNATURE, hmac_hex)
    return hmac_password

def before_user_insert(object_name, data, access_type):
    assert object_name == COSMOS_USERS_OBJECT_NAME
    assert isinstance(data, dict)
    assert access_type == AccessType.INSERT or access_type == AccessType.UPDATE

    password = data.get(PASSWORD_COLUMN_NAME)

    if not password:
        return

    if password.find(PASSWORD_HMAC_SIGNATURE) > 0:
        return

    hmac_password = get_hmac_password(password)

    data[PASSWORD_COLUMN_NAME] = hmac_password