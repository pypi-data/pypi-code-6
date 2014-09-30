from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend as SmtpEmailBackend


class EmailBackend(SmtpEmailBackend):
    def __init__(self, *args, **kwargs):
        fail_silently = kwargs.pop('fail_silently', False)
        kwargs['fail_silently'] = False
        super(EmailBackend, self).__init__(*args, **kwargs)
        kwargs['fail_silently'] = fail_silently

        host = getattr(settings, 'ALTERNATIVE_EMAIL_HOST', None)
        port = getattr(settings, 'ALTERNATIVE_EMAIL_PORT', None)

        if host is not None and port is not None and host != self.host and port != self.port:
            username = getattr(settings, 'ALTERNATIVE_EMAIL_HOST_USER', None)
            password = getattr(settings, 'ALTERNATIVE_EMAIL_HOST_PASSWORD', None)
            use_tls = getattr(settings, 'ALTERNATIVE_EMAIL_USE_TLS', None)
            self._alternative_backend = SmtpEmailBackend(
                host=host,
                port=port,
                username=username,
                password=password,
                use_tls=use_tls,
                **kwargs
            )
        else:
            self._alternative_backend = None

    def send_messages(self, email_messages):
        try:
            return super(EmailBackend, self).send_messages(email_messages)
        except Exception as e:
            if self._alternative_backend:
                return self._alternative_backend.send_messages(email_messages)
            else:
                raise e

