from django.contrib.auth.models import User
from django.conf import settings

AUTO_CREATE_ADMIN = getattr(settings, 'COMMON_AUTO_CREATE_ADMIN', True)
AUTO_ADMIN_USERNAME = getattr(settings, 'COMMON_AUTO_ADMIN_USERNAME', u'admin')
AUTO_ADMIN_PASSWORD = getattr(settings, 'COMMON_AUTO_ADMIN_PASSWORD', User.objects.make_random_password())
