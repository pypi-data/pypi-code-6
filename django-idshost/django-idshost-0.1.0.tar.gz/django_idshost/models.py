from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


class IdsManager(UserManager):

    def create_user(self, username, cert_mask=None, email=None, password=None,
                    commit=True, **extra_fields):
        user = super(IdsManager, self).create_user(username, email, password,
                                                   **extra_fields)

        auth = '03{name}'.format(name=username)
        user.ids_authentifier = auth
        if commit:
            user.save(using=self._db)
        return user


class IdsUser(AbstractUser):

    ids_authentifier = models.CharField(
        _('ids authentifier'), max_length=100, unique=True,
        null=True, blank=True)
    REQUIRED_FIELDS = ['ids_authentifier']
    objects = IdsManager()
