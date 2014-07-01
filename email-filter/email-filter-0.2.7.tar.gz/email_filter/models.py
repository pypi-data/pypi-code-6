# -*- coding: utf-8 -*-
import chardet
import datetime
from functools import partial

from django.conf import settings
from django.db import models

from email.utils import parseaddr


def get_cleaned_email(email):
    return parseaddr(email)[1]


def get_name_from_email(email):
    email = get_cleaned_email(email)
    if '@' in email:
        return email.split('@')[0]
    return ''


def is_local_email(email_address):
    email_servers = getattr(settings, 'EMAIL_SERVER_DOMAINS', ['@42cc.co'])
    for server in email_servers:
        if email_address.endswith(server):
            return True
    return False


def is_project_recipient(recipient):
    """
    Returns True is recipient has valid email (ends with @company.mail.domain.mine)
    """
    email = get_cleaned_email(recipient)
    return is_local_email(email)


class ERManager(models.Manager):
    def get_object_or_None(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None

    def get_or_create_back_email(self, email):
        email_server = getattr(settings, 'EMAIL_SERVER_DOMAINS', ['@42cc.co'])[0]
        return_email = self.get_object_or_None(email_in=email)
        if return_email is None:
            er = self.create(
                email_in=email,
                email_redirect='username@mail.com',
            )
            return_email = '%s__%s%s' % (get_name_from_email(email), er.id, email_server)
            er.email_redirect = return_email
            er.save()
        else:
            return_email = return_email.email_redirect
        return return_email

    def get_original_from_back_email(self, email):
        # be on the safe side, use filter instead of get
        ers = self.filter(email_redirect=email)
        if ers.exists():
            return ers[0].email_in
        return None


class EmailRedirect(models.Model):

    email_in = models.EmailField(max_length=250, unique=True)
    email_redirect = models.EmailField(max_length=250)
    objects = ERManager()

    class Meta:
        unique_together = ('email_in', 'email_redirect')

    def __unicode__(self):
        return '[%s] %s -> %s' % (self.id, self.email_in, self.email_redirect)

    @classmethod
    def get_server_email_domain(cls):
        return getattr(settings, 'EMAIL_SERVER_DOMAINS', ['@42cc.co'])[0]

    def save(self, *args, **kwargs):
        self.email_in = get_cleaned_email(self.email_in)
        super(EmailRedirect, self).save(*args, **kwargs)


def upload_to_date(instance, filename, prefix):
    month_number = int(datetime.date.today().toordinal()/30)
    return '{prefix}/{month_number}/{filename}'.format(
        prefix=prefix, filename=filename, month_number=month_number,
        instance=instance
    )


class EmailLog(models.Model):
    sender = models.EmailField(max_length=250)
    recipient = models.CharField(max_length=750)
    subject = models.CharField(max_length=255)
    raw_body = models.TextField()
    raw_email = models.FileField(upload_to=partial(upload_to_date, prefix='files/emails'), null=True)
    message_id = models.CharField(max_length=255, default='', blank=True)
    in_reply_to = models.CharField(max_length=255, default='', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return '[%s] %s' % (self.id, self.subject)

    def save(self, *args, **kwargs):
        decode = kwargs.get('decode', True)
        if decode and self.raw_body and not isinstance(self.raw_body, unicode):
            for body_charset in 'koi8-r', 'latin-1', 'utf-8', 'ascii':
                try:
                    self.raw_body = self.raw_body.decode(body_charset)
                except:
                    pass
                else:
                    break
            # self.raw_body = self.raw_body.decode(
            #     chardet.detect(self.raw_body)['encoding'])
        super(EmailLog, self).save(*args, **kwargs)


class EmailAttachment(models.Model):
    attachment = models.FileField(upload_to=partial(upload_to_date, prefix='files/email_attaches'), null=False)
    email_log = models.ForeignKey(EmailLog, related_name='attachments')
