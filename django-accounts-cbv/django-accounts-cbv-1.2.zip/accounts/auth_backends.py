from django.contrib.auth.backends import ModelBackend
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    get_user_model = lambda: User
import re


email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain


class EmailBackend(ModelBackend):
    UserModel = get_user_model()

    """Authenticate using email only"""
    def authenticate(self, username=None, password=None):
        if email_re.search(username):
            try:
                user = self.UserModel.objects.get(email=username)
                if user.check_password(password):
                    return user
            except self.UserModel.DoesNotExist:
                pass
        return None
