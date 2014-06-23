from django.db import models
from django.conf import settings
from oauth2client.django_orm import CredentialsField


class GoogleModel(models.Model):
    def disconnect_twitter(self):
        try:
            tp = GoogleProfile.objects.get(user=self)
            tp.delete()
        except GoogleProfile.DoesNotExist:
            pass

    class Meta:
        abstract = True


class GoogleProfile(models.Model):
    """
        An example Profile model that handles storing the oauth_token and
        oauth_secret in relation to a user. Adapt this if you have a current
        setup, there's really nothing special going on here.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    credential = CredentialsField()
