import hashlib
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.db import models
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from .utils import send_email

# app settings
if not hasattr(settings, 'SIGNUP_ACTIVATION_DAYS'):
	settings.SIGNUP_ACTIVATION_DAYS = 2
if not hasattr(settings, 'SIGNUP_FORM_CLASS'):
	settings.SIGNUP_FORM_CLASS = None
if not hasattr(settings, 'SIGNUP_ALLOWED'):
	settings.SIGNUP_ALLOWED = True

class ValidationManager(models.Manager):
	def create_validation(self, user):
		v = Validation(user=user)

		salt = get_random_string()
		# we encode it to utf-8 and ignore any stray input to be able to
		# hash the string
		to_hash = (salt + user.get_full_name()).encode('utf-8', 'ignore')
		key = hashlib.sha256(to_hash).hexdigest()

		v.key = key
		v.save(using=self._db)
		return v
	
	def create_inactive_user(self, **kwargs):
		UserModel = get_user_model()

		# use whatever password field the form had (because at this point, the
		# form has already been validated) and ditch the other fields if they
		# exist, because create_user won't accept those
		for p in ['password', 'password1', 'password2']:
			if kwargs.get(p):
				kwargs['password'] = kwargs[p]
				break
		for p in ['password1', 'password2']:
			kwargs.pop(p, None)

		user = UserModel.objects.create_user(**kwargs)
		user.is_active = False
		user.save(using=self._db)

		return user
	
class Validation(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)
	key = models.CharField(max_length=64)
	created = models.DateTimeField(auto_now_add=True)

	objects = ValidationManager()

	def get_activation_url(self, site):
		url = "http://%(site)s%(path)s" % {
			'site': site,
			'path': reverse('signup_activate', kwargs={'activation_key': self.key})
		}

		return url

	def send_activation_email(self, site):
		template_name = 'registration/activation_email.txt'

		# context data
		url = self.get_activation_url(site)
		context = {
			'site': site,
			'url': url,
			'activation_days': settings.SIGNUP_ACTIVATION_DAYS
		}

		to = self.user.email

		send_email(template_name, context, to)
	
	def activate_user(self):
		self.user.is_active = True
		self.user.save()

