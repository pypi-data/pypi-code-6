# -*- coding: utf-8 -*-
import json
import logging
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.core.mail.message import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template import Template, RequestContext
from django.template.base import TemplateDoesNotExist
from django.template.loader import get_template
from django.test import RequestFactory
from django.utils.translation import ugettext_lazy as _, get_language, activate


log = logging.getLogger(__name__)

DEFAULT_SENDER_EMAIL = getattr(settings, 'MAILTO_DEFAULT_SENDER_EMAIL', settings.DEFAULT_FROM_EMAIL)
TEMPLATE_CHOICES = getattr(settings, 'MAILTO_TEMPLATES', (
    ('mailto/default.html', _('Default')),
    ('mailto/default_2col.html', _('Default 2 column')),
    ('mailto/default_3col.html', _('Default 3 column')),
))
LANGUAGE_CHOICES = sorted(settings.LANGUAGES, key=lambda i: i[1])


def get_request(url='/'):
    """
    Returns fake HttpRequest object for rendering purpose.
    """
    defaults = {}

    site = Site.objects.get_current()
    defaults['SERVER_NAME'] = str(site.domain.split(':')[0])

    try:
        defaults['SERVER_PORT'] = str(site.domain.split(':')[1])
    except IndexError:
        pass

    return RequestFactory(**defaults).get(url)


class UserOptin(models.Model):
    user = models.OneToOneField(User, related_name='optin')
    optin = models.BooleanField(_('Optin'), default=True)
    date_added = models.DateTimeField(_('Date added'), auto_now_add=True)
    date_changed = models.DateTimeField(_('Date changed'), auto_now=True)
    hash = models.CharField(_('Hash'), max_length=32, unique=True, default=uuid.uuid4().hex)

    class Meta:
        verbose_name = _('Optin')
        verbose_name_plural = _('Optins')

    def __unicode__(self):
        return self.user.username

    @classmethod
    def get_emails(cls, emails):
        """
        Retruns set of recipient emails under consideration of optins.
        """
        optins = cls.objects.filter(user__email__in=emails)
        known_emails = optins.values_list('user__email', flat=True)
        emails_with_optin = optins.filter(optin=True).values_list('user__email', flat=True)
        unknown_emails = set(emails) - set(known_emails)
        return set(emails_with_optin) | set(unknown_emails)

    def get_optout_url(self):
        return get_request().build_absolute_uri(reverse('optout', kwargs={'hash': self.hash}))


@receiver(post_save, sender=User)
def create_user_optin(sender, **kwargs):
    if kwargs.get('created', False):
        user_optin = UserOptin()
        user_optin.user = kwargs.get('instance')
        user_optin.save()


class Mail(models.Model):
    active = models.BooleanField(_('Active'), default=False)
    slug = models.SlugField(_('Slug'))
    language_code = models.CharField(_('Language'), max_length=7, choices=LANGUAGE_CHOICES,
                                     default=settings.LANGUAGE_CODE)

    sender_name = models.CharField(_('Sender Name'), max_length=255, blank=True, null=True, default=None)
    sender_email = models.EmailField(_('Sender Email Address'), default=DEFAULT_SENDER_EMAIL)
    reply_to = models.EmailField(_('Reply To'), blank=True, null=True, default=None)
    # TODO: Email validation
    cc = models.CharField(_('CC Recipients'), max_length=1024, blank=True, null=True, default=None,
                          help_text=_('Comma separated list of CC recipients.'))
    # TODO: Email validation
    bcc = models.CharField(_('BCC Recipients'), max_length=1024, blank=True, null=True, default=None,
                           help_text=_('Comma separated list of BCC recipients.'))

    subject = models.CharField(_('Subject'), max_length=512)
    plain = models.TextField(_('Plain Content'))
    html = models.TextField(_('HTML Content'), blank=True, null=True, default=None)

    template = models.CharField(_('Template'), max_length=1024, choices=TEMPLATE_CHOICES, default='mailto/default.html')
    optout = models.BooleanField(_('Optout'), default=True,
                                 help_text=_('Indicates if this Email can be unsubscribed by user.'))

    class Meta:
        unique_together = (('slug', 'language_code'), )

    def __unicode__(self):
        return self.slug

    @classmethod
    def register(cls, slug, language_code=settings.LANGUAGE_CODE):
        """
        Get and/or create Mail object.
        """
        try:
            mail = cls.objects.get(slug=slug, language_code=language_code)
        except ObjectDoesNotExist:
            mail = cls()
            mail.slug = slug
            mail.language_code = language_code
            mail.subject = slug
            mail.plain = slug
            mail.save()
            log.info(u'Mail with slug `%s` created.' % slug)
        return mail

    def get_subject(self, context):
        """
        Returns rendered subject.
        """
        tpl = Template(self.subject)
        ctx = RequestContext(get_request(), context)
        return tpl.render(ctx)

    def get_plain_content(self, context):
        """
        Returns rendered plain email body.
        """
        tpl = Template(self.plain)
        ctx = RequestContext(get_request(), context)

        try:
            # Try to get and render base plain template
            base_tpl_name = self.template.split('.')[:-1]
            base_tpl_name.append('txt')
            base_tpl_name = '.'.join(base_tpl_name)

            base_context = context
            base_context.update({
                'body': tpl.render(ctx)
            })
            base_tpl = get_template(base_tpl_name)
            base_ctx = RequestContext(get_request(), base_context)
            return base_tpl.render(base_ctx)

        except TemplateDoesNotExist:
            return tpl.render(ctx)

    def get_html_content(self, context):
        """
        Returns rendered HTML email body.
        """
        if not self.html:
            return None

        base_ctx = RequestContext(get_request(), json.loads(self.html))
        base_tpl = get_template(self.template)

        tpl = Template(base_tpl.render(base_ctx))
        ctx = RequestContext(get_request(), context)

        return tpl.render(ctx)

    def get_from_email(self):
        """
        Returns email address with name.
        """
        if self.sender_name:
            return '%s <%s>' % (self.sender_name, self.sender_email)
        else:
            return self.sender_email

    def get_cc_recipients(self):
        """
        Returns list of cc recipients.
        """
        if not self.cc:
            return []

        return [cc.strip() for cc in self.cc.split(',')]

    def get_bcc_recipeints(self):
        """
        Return list of bcc recipients.
        """
        if not self.bcc:
            return []

        return [bcc.strip() for bcc in self.bcc.split(',')]

    def send(self, recipients, context=None, from_email=None, reply_to=None, cc=[], bcc=[], headers={}, attachments=[]):
        """
        Constructs and sends message.
        """
        if not self.active:
            return

        recipient_emails = UserOptin.get_emails(recipients)
        if not recipient_emails or len(recipient_emails) == 0:
            return

        mail_kwargs = {
            'from_email': from_email if from_email else self.get_from_email(),
            'to': recipient_emails,
            'cc': self.get_cc_recipients() + cc if cc else self.get_cc_recipients(),
            'bcc': self.get_bcc_recipeints() + bcc if bcc else self.get_bcc_recipeints(),
            'headers': headers,
            'attachments': attachments
        }

        if self.reply_to:
            mail_kwargs['headers']['Reply-To'] = reply_to if reply_to else self.reply_to

        current_language = get_language()
        activate(self.language_code)

        mail_kwargs['subject'] = self.get_subject(context)

        context.update({
            'subject': mail_kwargs['subject']
        })

        mail_kwargs['body'] = self.get_plain_content(context)

        html = self.get_html_content(context)
        if html:
            mail_kwargs['alternatives'] = [(html, 'text/html'), ]

        activate(current_language)

        if mail_kwargs:
            email = EmailMultiAlternatives(**mail_kwargs)
        else:
            email = EmailMessage(**mail_kwargs)

        email.send()

    def preview_html(self):
        """
        Returns rendered HTML email body for preview.
        """
        tpl = get_template(self.template)
        ctx = RequestContext(get_request(), {
            'body_html': self.html
        })
        return tpl.render(ctx)


def mailto(recipients, slug, language_code=settings.LANGUAGE_CODE, context={}, **kwargs):
    try:
        context['recipient'] = User.objects.get(email__iexact=recipients[0])
    except ObjectDoesNotExist, IndexError:
        context['recipient'] = User(email=recipients[0])

    mail = Mail.register(slug, language_code)
    mail.send(recipients, context, **kwargs)