from django.db import models
from django.contrib.auth.models import User


class Token(models.Model):
    user   = models.ForeignKey(User)
    keyId  = models.CharField(max_length=64)
    secret = models.CharField(max_length=64)
