from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User

AUTO_ADMIN_PASSWORD = getattr(settings, 'COMMON_AUTO_ADMIN_PASSWORD', User.objects.make_random_password())
AUTO_ADMIN_USERNAME = getattr(settings, 'COMMON_AUTO_ADMIN_USERNAME', 'admin')
AUTO_CREATE_ADMIN = getattr(settings, 'COMMON_AUTO_CREATE_ADMIN', True)
