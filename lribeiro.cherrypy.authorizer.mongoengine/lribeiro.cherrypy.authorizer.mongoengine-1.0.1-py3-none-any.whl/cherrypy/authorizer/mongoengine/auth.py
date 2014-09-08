import bcrypt
import cherrypy
from lribeiro.cherrypy.authorizer.authentication import Identity, AuthenticationError

from lribeiro.cherrypy.authorizer.mongoengine.models import User, Resource


def authenticator(email: str, password: str) -> Identity:
    """
    Authenticate the user with email and password

    :param email: The user email
    :param password: The user password
    :return: The user Identity
    :rtype: Identity
    """
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise AuthenticationError()

    hashed = user.password.encode('utf-8')  # encoding th estring is required for bcrypt

    if not user or not bcrypt.hashpw(password.encode('utf-8'), hashed) == hashed:
        raise AuthenticationError()

    return Identity(user.email, user.name, user)


def authorizer(claims: dict) -> bool:
    """
    Verifies whether the user is authorized based on the given claims

    :param claims: A dict containing the authorization claims
    :type claims: dict
    :return: Whether the user is authorized
    :rtype: bool
    """
    identity = cherrypy.request.auth_user

    try:
        user = User.objects.get(email=identity.id)
    except User.DoesNotExist:
        return False

    for action, resource in claims.items():
        satisfied = False

        if isinstance(resource, str):
            for permission in user.permissions:
                if permission.action == action and permission.resource.name == resource:
                    satisfied = True

        elif isinstance(resource, list):
            found_permissions = list()

            for permission in user.permissions:
                if permission.action == action and permission.resource.name in resource:
                    found_permissions.append(permission)

            satisfied = len(found_permissions) == len(resource)

        if not satisfied:
            return False

    return True