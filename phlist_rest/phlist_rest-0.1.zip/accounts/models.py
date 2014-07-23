import re
import warnings
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, SiteProfileNotAvailable, PermissionsMixin
from django.core import validators
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from userena import settings as userena_settings
from userena.models import UserenaBaseProfile
from userena.utils import get_gravatar

from addresses.models import City


# Custom Phlist User manager
class PhlistUserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = PhlistUserManager.normalize_email(email)
        user = self.model(username=username,
                          email=email,
                          first_name=first_name,
                          last_name=last_name,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password, **extra_fields):
        u = self.create_user(username, email, first_name, last_name, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


# Custom Phlist User model
class PhlistUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user definition for Phlist.com
    """
    """ constants """
    USERNAME_MAX_LENGTH = 30
    FIRSTNAME_MAX_LENGTH = 30
    LASTNAME_MAX_LENGTH = 30
    EMAIL_MAX_LENGTH = 254
    MEMBER_TYPE_CHOICES = (
        ('N', 'Normal'),
        ('P', 'Paid'),
        ('B', 'Banned'),
    )

    """ fields """
    username = models.CharField(_('username'), max_length=USERNAME_MAX_LENGTH, unique=True, editable=False,
                                help_text=_('Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
                                validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
                                                                      _('Enter a valid username.'), 
                                                                      'invalid')])
    first_name = models.CharField(_('first name'), max_length=FIRSTNAME_MAX_LENGTH, blank=True)
    last_name = models.CharField(_('last name'), max_length=LASTNAME_MAX_LENGTH, blank=True)
    email = models.EmailField(_('email address'), max_length=EMAIL_MAX_LENGTH, unique=True, blank=True)
    member_type = models.CharField('member_type', max_length=1, choices=MEMBER_TYPE_CHOICES, default='N')
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = PhlistUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    """ meta """
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    """ methods """
    def __unicode__(self):
        return '%(username)s' % {'username': self.username}

    def check_new_ad_allowed(self):
        allowed = True
        num_ads = self.ads.aggregate(Count('id'))['id__count']
        # number of ad at limit
        if (num_ads >= settings.AD_LIMIT_PER_USER):
            allowed = False
        # user is banned
        if (self.member_type == 'B'):
            allowed = False
        return allowed

    def get_absolute_url(self):
        return reverse('userena_profile_detail', args=(self.username,))

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def get_profile(self):
        """
        Returns site-specific profile for this user. Raises
        SiteProfileNotAvailable if this site does not allow profiles.
        """
        warnings.warn("The use of AUTH_PROFILE_MODULE to define user profiles has been deprecated.",
            PendingDeprecationWarning)
        if not hasattr(self, '_profile_cache'):
            from django.conf import settings
            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable(
                    'You need to set AUTH_PROFILE_MODULE in your project '
                    'settings')
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable(
                    'app_label and model_name should be separated by a dot in '
                    'the AUTH_PROFILE_MODULE setting')
            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable(
                        'Unable to load the profile model, check '
                        'AUTH_PROFILE_MODULE in your project settings')
                self._profile_cache = model._default_manager.using(
                                   self._state.db).get(user__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache

    def set_banned(self):
        self.member_type = 'B'
        self.is_active = False
        self.save()
        self.ads.select_for_update().filter(is_active=True).update(is_active=False)


# Userena Profile
class PhlistProfile(UserenaBaseProfile):
    """
    Custom user profile for Phlist.com
    """
    """ constants """
    ADDRESSLINE1_MAX_LENGTH = 100
    ZIPCODE_MAX_LENGTH = 8
    CONTACTNUM_MAX_LENGTH = 20

    """ fields """
    ip_address = models.IPAddressField(blank=True, null=True)
    address_line1 = models.CharField(max_length=ADDRESSLINE1_MAX_LENGTH, blank=True)
    zip_code = models.CharField(max_length=ZIPCODE_MAX_LENGTH, blank=True)
    city = models.ForeignKey(City, null=True, to_field='slug')
    contact_num = models.CharField(max_length=CONTACTNUM_MAX_LENGTH, blank=True)
    legacy_user_id = models.IntegerField(blank=True, null=True)

    """ meta """
    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    """ methods """
    def __unicode__(self):
        return '%(username)s' % {'username': self.user.username}

    def get_mugshot_url(self, width=0):
        if self.image:
            url = self.image.url
        else:
            if width <= 0:
                width = userena_settings.USERENA_MUGSHOT_SIZE
            url = get_gravatar(self.user.email,
                               width,
                               userena_settings.USERENA_MUGSHOT_DEFAULT)
        return url

    def get_absolute_url(self):
        return reverse('userena_profile_detail', args=(self.user.username,)) 

    def get_gender_label(self):
        s = 'Not Specified'
        if self.gender == 'm':
            s = 'Male'
        elif self.gender == 'f':
            s = 'Female'
        return s

    def get_privacy_label(self):
        s = 'Everyone'
        if self.privacy == 'registered':
            s = 'Registered Users Only'
        elif self.privacy == 'closed':
            s = 'No One'
        return s
