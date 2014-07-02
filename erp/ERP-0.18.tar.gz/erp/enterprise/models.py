import re
from django.db import models
from django.conf import settings
from django.db.models.signals import class_prepared
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, GroupManager, Group, PermissionsMixin
)


SEX_CHOICES = (
    ('m', 'Мужской'),
    ('f', 'Женский'),
)


def hijack(**kwargs):
        """
        Hijaking auth model to get permissions through CorpUnit
        insted of basic groups. Just changes foreign key.
        """
        groups = models.ManyToManyField(CorpUnit, verbose_name='Подразделение',
                                        blank=True, help_text='The groups this user belongs to. A user will '
                                        'get all permissions granted to each of ''his/her group.',
                                        related_name="corp_user_set", related_query_name="user")
        groups.contribute_to_class(PermissionsMixin, 'groups')


class CorpUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            password=password,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CorpObject(models.Model):
    name = models.CharField(max_length=15)
    lat = models.FloatField('Latitude', blank=True, null=True)
    lng = models.FloatField('Longitude', blank=True, null=True)
    #value = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey('CorpObject', blank=True, null=True)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    building = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('obj-detail', args=[str(self.id)])


class CorpUnit(Group):
    chief = models.ForeignKey('CorpUser')
    obj = models.ForeignKey(CorpObject, blank=True, null=True)
    #value = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey('CorpUnit', blank=True, null=True)

    objects = GroupManager()

    # On Python 3: def __str__(self):
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('unit-detail', args=[str(self.id)])


class CorpUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Имя пользователя', max_length=30, unique=True)
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True)
    mid_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Отчетво')
    sex = models.CharField(choices=SEX_CHOICES, max_length=1, blank=True)
    email = models.EmailField('Адрес почты', blank=True)
    avatar = models.ImageField(upload_to=settings.MEDIA_ROOT + 'users/avatar', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    corp_group = models.ForeignKey(CorpUnit, blank=True, null=True, verbose_name='Подразделение')
    phone = models.CharField(max_length=12, blank=True, null=True, verbose_name='Телефон')

    objects = CorpUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        #TODO: self.first_name + '' + self_last_name
        return self.username

    def get_short_name(self):
        #TODO: self.first_name
        return self.username

    # On Python 3: def __str__(self):
    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    class_prepared.connect(hijack)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('user-detail', args=[str(self.id)])

    @property
    def url(self):
        from django.core.urlresolvers import reverse
        return reverse('user-detail', args=[str(self.id)])


#TODO: uncomment
# class Role(models.Model):
#     user = models.ForeignKey(CorpUser)
#     unit = models.ForeignKey(CorpUnit)
#     position = models.CharField('Должность', max_length=30)
#
#     def __str__(self):
#         return self.user.username