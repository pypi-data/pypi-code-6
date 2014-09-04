import bcrypt
import cherrypy
from lribeiro.cherrypy.authorizer.authentication import Identity, AuthenticationError

from lribeiro.cherrypy.authorizer.mongoengine.models import User


def authenticator(email: str, password: str) -> Identity:
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise AuthenticationError()

    hashed = user.password.encode('utf-8')  # encoding th estring is required for bcrypt

    if not user or not bcrypt.hashpw(password.encode('utf-8'), hashed) == hashed:
        raise AuthenticationError()

    return Identity(user.email, user.name, user)


def authorizer(claims: dict) -> bool:
    identity = cherrypy.request.auth_user

    try:
        user = User.objects.get(email=identity.id)
    except User.DoesNotExist:
        return False

    for action, resource in claims.items():
        satisfied = False
        for permission in user.permissions:
            if permission.action == action and permission.resource.name == resource:
                satisfied = True

        if not satisfied:
            return False

    return True