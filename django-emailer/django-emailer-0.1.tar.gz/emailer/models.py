from smtplib import SMTP

from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives, get_connection
from django.db import models
from django.template import Context, Template
from django.template.defaultfilters import mark_safe, striptags
from django.template.loader import get_template


class ConnectionProfile(models.Model):
    host = models.CharField(max_length=60)
    username = models.CharField(max_length=40, blank=True)
    password = models.CharField(max_length=40, blank=True)
    port = models.PositiveSmallIntegerField()
    use_tls = models.BooleanField(default=True)

    def __str__(self):
        return '{username} @ {host}:{port}'.format(**vars(self))

    def clean(self):
        try:
            smtp = SMTP()
            smtp.connect(self.host, self.port)
            self.use_tls and smtp.starttls()
            self.username and smtp.login(self.username, self.password)
        except Exception as err:
            raise ValidationError(str(err))


class EmailTemplate(models.Model):
    name = models.SlugField(primary_key=True)
    connection_profile = models.ForeignKey('ConnectionProfile')
    base_template_name = models.CharField(
        max_length=70, blank=True, default='email/default.html')
    subject = models.CharField(max_length=40)
    content = models.TextField()

    @staticmethod
    def get(name):
        return EmailTemplate.objects.get(name=name)

    def __unicode__(self):
        return self.subject

    def clean(self):
        self.name = self.name.upper()

    def render(self, to, context, from_email=''):
        context = Context(dict(context, subject=self.subject))
        subject = Template(self.subject).render(context)
        base_template = get_template(self.base_template_name)
        content = mark_safe(Template(self.content).render(context))
        body = base_template.render(Context({'content': content}))

        connection = get_connection()
        connection.__dict__.update(**{
            field: getattr(self.connection_profile, field)
            for field in ('host', 'port', 'use_tls', 'username', 'password',)})

        # accept a single email as a string
        if not isinstance(to, (list, tuple)):
            to = [to]

        email = EmailMultiAlternatives(
            subject, striptags(body), from_email, to, connection=connection)
        email.attach_alternative(body, 'text/html')

        return email
